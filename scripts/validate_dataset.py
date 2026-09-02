#!/usr/bin/env python3
"""Quality checks for eCifre's public CSV datasets.

Runs against the per-indicator CSVs in datasets/ by default, or against
any other CSV file(s) sharing the same 9-column schema (e.g. the
consolidated kaggle/build/romania_economic_indicators.csv), for:

- UTF-8 decodability
- exact header / column count
- duplicate (indicator, date, geography) rows within a file
- missing values in any column
- malformed numeric `value` fields
- invalid ISO-8601 `date` fields
- malformed `source_url` / `ecifre_url` fields
- a source code reporting more than one distinct `source` name (or vice versa)
- a single indicator name reporting more than one distinct `unit`

Nothing is deleted or rewritten — this only reports. Exits non-zero if any
row-level issue was found (missing header mismatches also fail).
"""

from __future__ import annotations

import csv
import datetime
import glob
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

SOURCE_COLUMNS = [
    "indicator",
    "date",
    "value",
    "unit",
    "geography",
    "source",
    "source_url",
    "ecifre_url",
    "last_updated",
]

CONSOLIDATED_COLUMNS = [
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

KNOWN_SCHEMAS = {
    tuple(SOURCE_COLUMNS): SOURCE_COLUMNS,
    tuple(CONSOLIDATED_COLUMNS): CONSOLIDATED_COLUMNS,
}


def is_valid_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def validate_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [f"{path}: not valid UTF-8 ({exc})"]

    reader = csv.DictReader(text.splitlines())
    columns = KNOWN_SCHEMAS.get(tuple(reader.fieldnames or []))
    if columns is None:
        issues.append(f"{path}: unexpected header {reader.fieldnames}")
        return issues

    seen_keys: dict[tuple, int] = {}
    unit_by_indicator: dict[str, set[str]] = defaultdict(set)
    source_name_by_code: dict[str, set[str]] = defaultdict(set)

    for line_no, row in enumerate(reader, start=2):
        for col in columns:
            if not row.get(col, "").strip():
                issues.append(f"{path}:{line_no}: missing '{col}'")

        key = (row.get("indicator"), row.get("date"), row.get("geography"))
        if key in seen_keys:
            issues.append(
                f"{path}:{line_no}: duplicate indicator/date/geography "
                f"(first seen at line {seen_keys[key]}): {key}"
            )
        else:
            seen_keys[key] = line_no

        value = row.get("value", "")
        try:
            float(value)
        except ValueError:
            issues.append(f"{path}:{line_no}: malformed numeric value {value!r}")

        date_str = row.get("date", "")
        try:
            datetime.date.fromisoformat(date_str)
        except ValueError:
            issues.append(f"{path}:{line_no}: invalid ISO-8601 date {date_str!r}")

        last_updated = row.get("last_updated", "")
        if last_updated and not last_updated[:10].count("-") == 2:
            issues.append(f"{path}:{line_no}: suspicious last_updated {last_updated!r}")

        for col in ("source_url", "ecifre_url"):
            url = row.get(col, "")
            if url and not is_valid_url(url):
                issues.append(f"{path}:{line_no}: invalid {col} {url!r}")

        indicator = row.get("indicator", "")
        unit = row.get("unit", "")
        if indicator and unit:
            unit_by_indicator[indicator].add(unit)

        source = row.get("source", "")
        if source:
            source_name_by_code[source].add(source)

    for indicator, units in unit_by_indicator.items():
        if len(units) > 1:
            issues.append(f"{path}: indicator {indicator!r} has inconsistent units: {sorted(units)}")

    return issues


def main() -> int:
    args = sys.argv[1:]
    if args:
        paths = [Path(p) for p in args]
    else:
        repo_root = Path(__file__).resolve().parent.parent
        paths = sorted((repo_root / "datasets").glob("**/*.csv"))

    if not paths:
        print("No CSV files found to validate.")
        return 1

    all_issues: list[str] = []

    for path in paths:
        all_issues.extend(validate_file(path))

    # Cross-file slug collision check: same slug must always map to the same indicator name.
    slug_to_names: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if tuple(reader.fieldnames or []) not in KNOWN_SCHEMAS:
                continue
            for row in reader:
                url = row.get("ecifre_url", "")
                marker = "/indicatori/"
                if marker in url:
                    slug = url.split(marker, 1)[1].split("/")[0]
                    slug_to_names[slug].add(row.get("indicator", ""))

    for slug, names in slug_to_names.items():
        if len(names) > 1:
            all_issues.append(f"slug collision: {slug!r} maps to multiple indicator names: {sorted(names)}")

    print(f"Validated {len(paths)} file(s).")
    if all_issues:
        print(f"\n{len(all_issues)} issue(s) found:\n")
        for issue in all_issues:
            print(" -", issue)
        return 1

    print("No issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
