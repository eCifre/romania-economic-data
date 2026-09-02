#!/usr/bin/env python3
"""Build, validate, and publish the eCifre dataset to Hugging Face.

Requires the `huggingface_hub` and `pyarrow` packages, and an
authenticated Hugging Face account via the HF_TOKEN environment variable
(or a prior `huggingface-cli login` / `hf auth login`). This script never
reads, writes, or logs the token itself — it's picked up implicitly by
huggingface_hub from the environment / local HF credential store.

Steps:
  1. Run scripts/build_canonical_dataset.py (the one shared build every
     platform uses — this script does not re-implement any normalization).
  2. Validate the output with scripts/validate_dataset.py.
  3. Convert to Parquet with scripts/csv_to_parquet.py.
  4. Compare a hash of the new build against the hash already published on
     Hugging Face (stored in a small `.build_hash` file in the dataset
     repo) — skip the upload entirely if nothing changed, unless --force
     is passed. This avoids meaningless no-op commits.
  5. Assemble a flat staging folder (huggingface/build/) with the dataset
     card, LICENSE, DATA_DICTIONARY.md, and both data files.
  6. Create the repo if it doesn't exist yet (public dataset repo), and
     upload the staging folder as one commit.

Usage:
    export HF_TOKEN=hf_...
    python3 scripts/publish_huggingface.py
    python3 scripts/publish_huggingface.py --message "Add Q3 2026 revisions"
    python3 scripts/publish_huggingface.py --force   # upload even if unchanged
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_ID = "ecifre/romania-economic-indicators"

BUILD_CSV = REPO_ROOT / "build" / "romania_economic_indicators.csv"
BUILD_PARQUET = REPO_ROOT / "build" / "romania_economic_indicators.parquet"
STAGE_DIR = REPO_ROOT / "huggingface" / "build"
HASH_FILENAME = ".build_hash"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--message", help="Commit message (default: auto-generated with today's date)")
    parser.add_argument("--force", action="store_true", help="Upload even if the build is unchanged")
    args = parser.parse_args()

    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("ERROR: huggingface_hub is not installed. Install it with: pip install huggingface_hub", file=sys.stderr)
        return 1

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)
    try:
        who = api.whoami()
    except Exception as exc:  # noqa: BLE001 - report auth failure clearly, no token in the message
        print(f"ERROR: not authenticated with Hugging Face ({exc.__class__.__name__}).", file=sys.stderr)
        print("Set HF_TOKEN, or run `hf auth login` / `huggingface-cli login` first.", file=sys.stderr)
        return 1
    print(f"Authenticated as: {who.get('name', '<unknown>')}", flush=True)

    print("\n== Build (canonical, shared with every platform) ==", flush=True)
    run([sys.executable, "scripts/build_canonical_dataset.py"])

    print("\n== Validate ==", flush=True)
    run([sys.executable, "scripts/validate_dataset.py", str(BUILD_CSV)])

    print("\n== Convert to Parquet ==", flush=True)
    run([sys.executable, "scripts/csv_to_parquet.py"])

    new_hash = sha256_of(BUILD_CSV)

    print("\n== Check for changes ==")
    api.create_repo(repo_id=REPO_ID, repo_type="dataset", private=False, exist_ok=True)

    remote_hash = None
    try:
        from huggingface_hub import hf_hub_download

        hash_path = hf_hub_download(repo_id=REPO_ID, repo_type="dataset", filename=HASH_FILENAME, token=token)
        remote_hash = Path(hash_path).read_text().strip()
    except Exception:
        remote_hash = None  # first-ever publish, or file not present yet

    if remote_hash == new_hash and not args.force:
        print("No changes since the last published version — skipping upload. Use --force to upload anyway.")
        return 0

    print("\n== Stage files ==")
    shutil.rmtree(STAGE_DIR, ignore_errors=True)
    STAGE_DIR.mkdir(parents=True)
    (STAGE_DIR / "data").mkdir()

    shutil.copy(REPO_ROOT / "huggingface" / "README.md", STAGE_DIR / "README.md")
    shutil.copy(REPO_ROOT / "huggingface" / "LICENSE", STAGE_DIR / "LICENSE")
    shutil.copy(REPO_ROOT / "DATA_DICTIONARY.md", STAGE_DIR / "DATA_DICTIONARY.md")
    shutil.copy(BUILD_CSV, STAGE_DIR / "data" / BUILD_CSV.name)
    shutil.copy(BUILD_PARQUET, STAGE_DIR / "data" / BUILD_PARQUET.name)
    (STAGE_DIR / HASH_FILENAME).write_text(new_hash)

    message = args.message or f"Update economic dataset — {date.today().isoformat()[:7]}"

    print(f"\n== Upload ({message!r}) ==")
    api.upload_folder(
        repo_id=REPO_ID,
        repo_type="dataset",
        folder_path=str(STAGE_DIR),
        commit_message=message,
    )

    shutil.rmtree(STAGE_DIR, ignore_errors=True)

    print(f"\nDone: https://huggingface.co/datasets/{REPO_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
