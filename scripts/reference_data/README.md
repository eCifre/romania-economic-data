# Reference data

Small, static lookup tables used by `scripts/build_kaggle_dataset.py` so the
build can run entirely from this repository, without calling any API at
build time.

- **`county_names.json`** — maps eCifre's geography codes (`RO-AB`, `RO-B`, …)
  to the official county name and an ASCII (diacritic-free) variant used in
  the consolidated Kaggle export. Snapshotted from `GET /api/v1/counties` on
  `https://api.ecifre.ro` (eCifre's public API) on 2026-09-02.

- **`indicator_metadata.json`** — maps each indicator's slug to its
  `frequency`, `unit`, `source` and `name` as published by eCifre. Snapshotted
  from `GET /api/v1/indicators/{slug}` on the same public API, same date,
  for exactly the 28 indicator slugs currently published under `datasets/`.

If new indicators are added to `datasets/`, add their entry to
`indicator_metadata.json` (the build script will fail loudly with a clear
error naming the missing slug(s) rather than silently emitting a blank
frequency).
