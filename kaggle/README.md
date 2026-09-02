# Romania Economic Indicators — Kaggle export

A structured collection of economic indicators for Romania, compiled and normalized by **[eCifre](https://ecifre.ro)** using data published by official Romanian and European institutions.

This folder is the packaging for that data as a Kaggle dataset. The dataset includes historical time series covering:

- GDP and economic growth
- inflation
- wages and salaries
- employment and unemployment
- exchange rates
- public finance
- construction
- energy
- population and county-level indicators

Interactive charts, current values, methodology and additional economic context for every indicator are available at **[ecifre.ro](https://ecifre.ro)**.

## What's in this folder

| Path | What it is |
| --- | --- |
| `dataset-metadata.json` | Kaggle dataset metadata (title, subtitle, license, keywords, resources) |
| `README.md` | This file |
| `DATA_DICTIONARY.md` | Column-by-column reference for the CSV |
| `LICENSE_NOTES.md` | Why the license isn't set yet, and what needs deciding |
| `build/romania_economic_indicators.csv` | The generated, consolidated dataset (built by `scripts/build_kaggle_dataset.py`) |

The per-indicator CSVs this is built from remain available individually under [`../datasets/`](../datasets/) — this consolidated file doesn't replace them, it's a single-file export for Kaggle.

## Structure

One row per (indicator, geography, date) observation, sorted by indicator, geography, then date. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for the full column reference.

- **Frequencies present:** daily, monthly, quarterly, annual, irregular
- **Geographies present:** `Romania` (national-level indicators) and all 42 Romanian counties (județe) plus București, by name (e.g. `Cluj`, `Timis`, `Bucuresti`) — diacritics removed for broader compatibility
- **Indicators:** 28, spanning inflation, GDP, wages, unemployment, exchange rates, public finance, construction, energy, and county-level demographics/business/GDP data

## Sources

Data in this export is derived from:

- **INSSE** — Institutul Național de Statistică
- **BNR** — Banca Națională a României
- **Eurostat**
- **Ministerul Finanțelor (MFIN)**
- **ANOFM** — Agenția Națională pentru Ocuparea Forței de Muncă
- **ANRE** — natural gas market data
- **ENTSO-E** — European electricity market transparency platform
- **ONRC** — Oficiul Național al Registrului Comerțului

Only institutions actually represented in this specific export are listed above — see the main repository's [DATA_SOURCES.md](../DATA_SOURCES.md) for the full list eCifre draws from (including sources deliberately excluded here for licensing reasons).

## Updates

This dataset is rebuilt from [github.com/eCifre/romania-economic-data](https://github.com/eCifre/romania-economic-data) via `scripts/build_kaggle_dataset.py`. `last_updated` (per row) reflects when eCifre's own pipeline last successfully refreshed that source, not when this particular Kaggle version was uploaded — check the Kaggle dataset's own version history for that.

## Limitations

- This is a subset of eCifre's full catalog (500+ indicators) — a representative starting set, not everything.
- A few indicators currently have very short histories (e.g. a single observation) because that's genuinely all that's been published so far by the source institution — not a data-loading bug.
- Two sources used elsewhere on eCifre (Bursa de Valori București / BVB, and OPCOM) are deliberately **excluded** from every eCifre dataset because their own terms require written consent for redistribution.

## Attribution

**eCifre — Romania Economic Indicators**
https://ecifre.ro

## Citation

If you use this dataset, attribution is appreciated:

> eCifre — Romania Economic Indicators. https://ecifre.ro

## Rebuilding and publishing

```bash
# Regenerate kaggle/build/romania_economic_indicators.csv from datasets/
python3 scripts/build_kaggle_dataset.py

# Check both the source CSVs and the consolidated export for issues
python3 scripts/validate_dataset.py
python3 scripts/validate_dataset.py kaggle/build/romania_economic_indicators.csv
```

Publishing requires the Kaggle CLI, authenticated locally — this repository never stores or transmits Kaggle credentials:

```bash
pipx install kaggle   # or: python3 -m venv .venv && .venv/bin/pip install kaggle

# Get an API token from https://www.kaggle.com/settings -> API -> Create New Token,
# which downloads kaggle.json. Then either:
mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json && chmod 600 ~/.kaggle/kaggle.json
# or export KAGGLE_USERNAME and KAGGLE_KEY as environment variables instead.
```

Before the first real publish, resolve the two placeholders in `dataset-metadata.json`:
- `"id"` — replace `REPLACE_WITH_KAGGLE_OWNER_SLUG` with the real Kaggle username or organization slug.
- `"licenses"` — replace the `DECISION-NEEDED-...` placeholder per [LICENSE_NOTES.md](LICENSE_NOTES.md).

Then:

```bash
scripts/publish_kaggle.sh create              # first-ever publish
scripts/publish_kaggle.sh version "message"    # later updates
```

Both build, validate, and refuse to run if either placeholder is still unresolved or no Kaggle credentials are found.

## About eCifre

eCifre is a Romanian economic data platform designed to make official economic information easier to discover, understand and compare: **[ecifre.ro](https://ecifre.ro)**
