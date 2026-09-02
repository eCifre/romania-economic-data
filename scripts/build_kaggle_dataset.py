#!/usr/bin/env python3
"""Build the consolidated Kaggle export from the public per-indicator CSVs.

Reads every CSV under datasets/, normalizes geography to a human-readable
name, attaches indicator_slug and frequency, and writes a single sorted
file to kaggle/build/romania_economic_indicators.csv.

This script only reads files already published in this repository
(datasets/) plus the small reference tables in scripts/reference_data/
(county names and indicator frequency, both snapshotted from eCifre's
public API — see scripts/reference_data/README.md). It does not call any
network API and does not touch eCifre's database, so it can be re-run by
anyone who has cloned this repository.

Usage:
    python3 scripts/build_kaggle_dataset.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
REFERENCE_DIR = REPO_ROOT / "scripts" / "reference_data"
OUTPUT_PATH = REPO_ROOT / "kaggle" / "build" / "romania_economic_indicators.csv"

OUTPUT_COLUMNS = [
    "indicator",
    "indicator_slug",
    "date",
    "value",
    "unit",
    "geography",
    "frequency",
    "source",
    "source_url",
    "ecifre_url",
    "last_updated",
]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def slug_from_ecifre_url(url: str) -> str:
    marker = "/indicatori/"
    if marker not in url:
        raise ValueError(f"cannot extract slug from ecifre_url: {url!r}")
    return url.split(marker, 1)[1].split("/")[0]


def geography_name(geo_code: str, county_names: dict) -> str:
    if geo_code == "RO":
        return "Romania"
    entry = county_names.get(geo_code)
    if entry is None:
        raise ValueError(f"unknown geography code: {geo_code!r} (not in reference_data/county_names.json)")
    return entry["name_ascii"]


def main() -> int:
    county_names = load_json(REFERENCE_DIR / "county_names.json")
    indicator_meta = load_json(REFERENCE_DIR / "indicator_metadata.json")

    csv_files = sorted(DATASETS_DIR.glob("**/*.csv"))
    if not csv_files:
        print("No source CSV files found under datasets/.", file=sys.stderr)
        return 1

    rows: list[dict] = []
    missing_frequency: set[str] = set()

    for path in csv_files:
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = slug_from_ecifre_url(row["ecifre_url"])
                frequency = indicator_meta.get(slug, {}).get("frequency")
                if frequency is None:
                    missing_frequency.add(slug)
                    frequency = ""
                rows.append(
                    {
                        "indicator": row["indicator"],
                        "indicator_slug": slug,
                        "date": row["date"],
                        "value": row["value"],
                        "unit": row["unit"],
                        "geography": geography_name(row["geography"], county_names),
                        "frequency": frequency,
                        "source": row["source"],
                        "source_url": row["source_url"],
                        "ecifre_url": row["ecifre_url"],
                        "last_updated": row["last_updated"],
                    }
                )

    if missing_frequency:
        print(
            "ERROR: missing frequency metadata for slug(s): "
            + ", ".join(sorted(missing_frequency))
            + "\nAdd them to scripts/reference_data/indicator_metadata.json before building.",
            file=sys.stderr,
        )
        return 1

    rows.sort(key=lambda r: (r["indicator_slug"], r["geography"], r["date"]))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    indicators = {r["indicator_slug"] for r in rows}
    geographies = {r["geography"] for r in rows}
    sources = {r["source"] for r in rows}
    dates = sorted(r["date"] for r in rows)

    print(f"Processed {len(csv_files)} source file(s) -> {OUTPUT_PATH}")
    print(f"Observations: {len(rows)}")
    print(f"Indicators:   {len(indicators)}")
    print(f"Geographies:  {len(geographies)}")
    print(f"Sources:      {len(sources)} ({', '.join(sorted(sources))})")
    print(f"Date range:   {dates[0]} -> {dates[-1]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
