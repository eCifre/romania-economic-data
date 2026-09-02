#!/usr/bin/env python3
"""Convert the canonical CSV to Parquet — serialization only, no data changes.

Parquet is a distribution format, not the canonical source: build/romania_economic_indicators.csv
(produced by build_canonical_dataset.py) remains the source of truth. This
script only re-encodes it with explicit column types (dates as real dates,
value as float64, everything else as string) for faster, more compact
loading in tools that prefer Parquet (Hugging Face Datasets, pandas, etc.).
No values are computed, rounded, filtered, or reordered.

Usage:
    python3 scripts/csv_to_parquet.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.csv as pa_csv
import pyarrow.parquet as pq

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = REPO_ROOT / "build" / "romania_economic_indicators.csv"
OUTPUT_PATH = REPO_ROOT / "build" / "romania_economic_indicators.parquet"

SCHEMA = pa.schema(
    [
        ("indicator", pa.string()),
        ("indicator_slug", pa.string()),
        ("date", pa.date32()),
        ("value", pa.float64()),
        ("unit", pa.string()),
        ("geography", pa.string()),
        ("frequency", pa.string()),
        ("source", pa.string()),
        ("source_url", pa.string()),
        ("ecifre_url", pa.string()),
        ("last_updated", pa.date32()),
    ]
)


def main() -> int:
    if not INPUT_PATH.exists():
        print(f"ERROR: {INPUT_PATH} does not exist. Run scripts/build_canonical_dataset.py first.", file=sys.stderr)
        return 1

    table = pa_csv.read_csv(
        INPUT_PATH,
        convert_options=pa_csv.ConvertOptions(
            column_types={name: pa.string() for name in SCHEMA.names},
        ),
    )

    # Re-cast from the all-string read into the real target schema.
    table = table.set_column(table.schema.get_field_index("date"), "date", table.column("date").cast(pa.date32()))
    table = table.set_column(
        table.schema.get_field_index("last_updated"), "last_updated", table.column("last_updated").cast(pa.date32())
    )
    table = table.set_column(table.schema.get_field_index("value"), "value", table.column("value").cast(pa.float64()))
    table = table.cast(SCHEMA)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, OUTPUT_PATH, compression="snappy")

    print(f"{INPUT_PATH} -> {OUTPUT_PATH}")
    print(f"Rows: {table.num_rows}, columns: {table.num_columns}")
    print(f"Size: {OUTPUT_PATH.stat().st_size / 1024:.1f} KiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
