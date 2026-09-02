#!/usr/bin/env python3
"""Build, validate, package, and publish the eCifre dataset to Zenodo.

Requires the `requests` package and a Zenodo personal access token in the
ZENODO_ACCESS_TOKEN environment variable (scopes: deposit:write,
deposit:actions). This script never reads, writes, or logs the token
itself beyond sending it in the Authorization header of each request.

Steps (matching the shared architecture — no data transformation happens
here that isn't already in build_canonical_dataset.py / csv_to_parquet.py):
  1. Run scripts/build_canonical_dataset.py.
  2. Validate with scripts/validate_dataset.py.
  3. Convert to Parquet with scripts/csv_to_parquet.py.
  4. Compute SHA-256 checksums (SHA256SUMS).
  5. Compare against the checksums already published in the latest Zenodo
     version (if any) — skip the release entirely if nothing changed,
     unless --force is passed.
  6. Assemble the release package (zenodo/build/): both data files, the
     Zenodo README, DATA_DICTIONARY.md, DATA_SOURCES.md, CHANGELOG.md,
     CITATION.cff, SHA256SUMS.
  7. Create a Zenodo deposition — a new record on the first-ever run, or
     a new version of the existing one (zenodo/.zenodo_record.json tracks
     which) — upload the metadata and files, and publish.
  8. Save the resulting DOI / concept DOI / record info to
     zenodo/.zenodo_record.json (this file is committed to git — it is
     not a secret, just which Zenodo record this repo publishes to).

Usage:
    export ZENODO_ACCESS_TOKEN=...
    python3 scripts/publish_zenodo.py                       # production
    python3 scripts/publish_zenodo.py --sandbox              # sandbox.zenodo.org, for testing the flow
    python3 scripts/publish_zenodo.py --version 2026.10
    python3 scripts/publish_zenodo.py --force
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

BUILD_CSV = REPO_ROOT / "build" / "romania_economic_indicators.csv"
BUILD_PARQUET = REPO_ROOT / "build" / "romania_economic_indicators.parquet"
STAGE_DIR = REPO_ROOT / "zenodo" / "build"
METADATA_TEMPLATE = REPO_ROOT / "zenodo" / "metadata.json"
RECORD_STATE_FILE = REPO_ROOT / "zenodo" / ".zenodo_record.json"
SHA256SUMS_NAME = "SHA256SUMS"

PACKAGE_STATIC_FILES = {
    REPO_ROOT / "zenodo" / "README.md": "README.md",
    REPO_ROOT / "DATA_DICTIONARY.md": "DATA_DICTIONARY.md",
    REPO_ROOT / "DATA_SOURCES.md": "DATA_SOURCES.md",
    REPO_ROOT / "zenodo" / "CHANGELOG.md": "CHANGELOG.md",
    REPO_ROOT / "CITATION.cff": "CITATION.cff",
}


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_record_state() -> dict:
    if RECORD_STATE_FILE.exists():
        return json.loads(RECORD_STATE_FILE.read_text())
    return {}


def save_record_state(state: dict) -> None:
    RECORD_STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", help="Release version, e.g. 2026.09 (default: current YYYY.MM)")
    parser.add_argument("--sandbox", action="store_true", help="Publish to sandbox.zenodo.org instead of production")
    parser.add_argument("--force", action="store_true", help="Publish even if the build is unchanged")
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("ERROR: requests is not installed. Install it with: pip install requests", file=sys.stderr)
        return 1

    import os

    token = os.environ.get("ZENODO_ACCESS_TOKEN")
    if not token:
        print("ERROR: ZENODO_ACCESS_TOKEN is not set.", file=sys.stderr)
        return 1

    base_url = "https://sandbox.zenodo.org/api" if args.sandbox else "https://zenodo.org/api"
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})

    version = args.version or date.today().strftime("%Y.%m")

    print("\n== Build (canonical, shared with every platform) ==", flush=True)
    run([sys.executable, "scripts/build_canonical_dataset.py"])

    print("\n== Validate ==", flush=True)
    run([sys.executable, "scripts/validate_dataset.py", str(BUILD_CSV)])

    print("\n== Convert to Parquet ==", flush=True)
    run([sys.executable, "scripts/csv_to_parquet.py"])

    print("\n== Checksums ==", flush=True)
    checksums = {
        BUILD_CSV.name: sha256_of(BUILD_CSV),
        BUILD_PARQUET.name: sha256_of(BUILD_PARQUET),
    }
    for name, digest in checksums.items():
        print(f"  {digest}  {name}")

    combined_hash = hashlib.sha256((checksums[BUILD_CSV.name] + checksums[BUILD_PARQUET.name]).encode()).hexdigest()

    state = load_record_state()
    latest_deposition_id = state.get("latest_deposition_id")

    print("\n== Check for changes ==", flush=True)
    if latest_deposition_id and state.get("build_hash") == combined_hash and not args.force:
        print("No changes since the last published version — skipping release. Use --force to publish anyway.")
        return 0
    if latest_deposition_id and state.get("build_hash") == combined_hash and args.force:
        print("Unchanged, but --force was passed — publishing a new version anyway.")

    print("\n== Stage release package ==", flush=True)
    shutil.rmtree(STAGE_DIR, ignore_errors=True)
    STAGE_DIR.mkdir(parents=True)
    for src, dest_name in PACKAGE_STATIC_FILES.items():
        shutil.copy(src, STAGE_DIR / dest_name)
    shutil.copy(BUILD_CSV, STAGE_DIR / BUILD_CSV.name)
    shutil.copy(BUILD_PARQUET, STAGE_DIR / BUILD_PARQUET.name)
    (STAGE_DIR / SHA256SUMS_NAME).write_text(
        "\n".join(f"{digest}  {name}" for name, digest in checksums.items()) + "\n"
    )

    metadata = json.loads(METADATA_TEMPLATE.read_text())
    metadata["version"] = version
    metadata["publication_date"] = date.today().isoformat()

    print(f"\n== {'New version' if latest_deposition_id else 'New deposition'} (version {version}) ==", flush=True)
    if latest_deposition_id:
        resp = session.post(f"{base_url}/deposit/depositions/{latest_deposition_id}/actions/newversion")
        resp.raise_for_status()
        draft_url = resp.json()["links"]["latest_draft"]
        resp = session.get(draft_url)
        resp.raise_for_status()
        draft = resp.json()
        deposition_id = draft["id"]

        # Zenodo carries the previous version's files into the new draft by
        # default — remove them before uploading the updated set, so we
        # don't end up with stale files alongside the new ones.
        for f in draft.get("files", []):
            del_resp = session.delete(f"{base_url}/deposit/depositions/{deposition_id}/files/{f['id']}")
            del_resp.raise_for_status()
    else:
        resp = session.post(f"{base_url}/deposit/depositions", json={})
        resp.raise_for_status()
        draft = resp.json()
        deposition_id = draft["id"]

    resp = session.put(f"{base_url}/deposit/depositions/{deposition_id}", json={"metadata": metadata})
    resp.raise_for_status()
    draft = resp.json()
    bucket_url = draft["links"]["bucket"]

    print("\n== Upload files ==", flush=True)
    for path in sorted(STAGE_DIR.iterdir()):
        print(f"  {path.name}", flush=True)
        with path.open("rb") as f:
            resp = session.put(f"{bucket_url}/{path.name}", data=f)
            resp.raise_for_status()

    print("\n== Publish ==", flush=True)
    resp = session.post(f"{base_url}/deposit/depositions/{deposition_id}/actions/publish")
    resp.raise_for_status()
    record = resp.json()

    state = {
        "sandbox": args.sandbox,
        "concept_recid": record.get("conceptrecid"),
        "concept_doi": record.get("conceptdoi"),
        "latest_deposition_id": record.get("id"),
        "latest_doi": record.get("doi"),
        "latest_version": version,
        "latest_record_url": record.get("links", {}).get("record_html") or record.get("links", {}).get("html"),
        "build_hash": combined_hash,
    }
    save_record_state(state)

    shutil.rmtree(STAGE_DIR, ignore_errors=True)

    print(f"\nDone. Version {version} published.")
    print(f"DOI: {state['latest_doi']}")
    print(f"Concept DOI: {state['concept_doi']}")
    print(f"Record URL: {state['latest_record_url']}")
    print(f"\nState saved to {RECORD_STATE_FILE.relative_to(REPO_ROOT)} — commit this file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
