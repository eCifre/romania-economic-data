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

The consolidated CSV this packages (`build/romania_economic_indicators.csv` at the repo root) is the same canonical export shared with every distribution platform (Kaggle, Hugging Face, and later Zenodo) — see [`../scripts/build_canonical_dataset.py`](../scripts/build_canonical_dataset.py). The column reference lives once, at the repo root: [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md). License reasoning: [`../LICENSE_NOTES.md`](../LICENSE_NOTES.md).

The per-indicator CSVs this is built from remain available individually under [`../datasets/`](../datasets/) — this consolidated file doesn't replace them, it's a single-file export for Kaggle.

## Structure

One row per (indicator, geography, date) observation, sorted by indicator, geography, then date. See [DATA_DICTIONARY.md](../DATA_DICTIONARY.md) for the full column reference.

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

This dataset is rebuilt from [github.com/eCifre/romania-economic-data](https://github.com/eCifre/romania-economic-data) via `scripts/build_canonical_dataset.py`. `last_updated` (per row) reflects when eCifre's own pipeline last successfully refreshed that source, not when this particular Kaggle version was uploaded — check the Kaggle dataset's own version history for that.

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
# Regenerate build/romania_economic_indicators.csv from datasets/
python3 scripts/build_canonical_dataset.py

# Check both the source CSVs and the consolidated export for issues
python3 scripts/validate_dataset.py
python3 scripts/validate_dataset.py build/romania_economic_indicators.csv
```

Publishing requires the Kaggle CLI, authenticated locally — this repository never stores or transmits Kaggle credentials:

```bash
pipx install kaggle   # or: python3 -m venv .venv && .venv/bin/pip install kaggle
```

Current Kaggle CLI versions (2.x) use a single API token rather than the older username+key pair. Generate one at https://www.kaggle.com/settings -> API -> Create New Token, then either:

```bash
export KAGGLE_API_TOKEN=<token>
```

or save it to `~/.kaggle/access_token` instead of exporting it every session. (The older `~/.kaggle/kaggle.json` with `KAGGLE_USERNAME`/`KAGGLE_KEY` still works too, if that's what you already have.)

`dataset-metadata.json`'s owner (`stefanvergu` — Kaggle has suspended organization creation platform-wide, so this publishes under a personal account rather than an eCifre org) and license (`"other"`, with the source-by-source terms spelled out in the `description` field — see [LICENSE_NOTES.md](../LICENSE_NOTES.md) for why) are already resolved. Then:

```bash
scripts/publish_kaggle.sh create              # first-ever publish
scripts/publish_kaggle.sh version "message"    # later updates
```

Both build and validate first, and refuse to run if no Kaggle credentials are found.

## About eCifre

eCifre is a Romanian economic data platform designed to make official economic information easier to discover, understand and compare: **[ecifre.ro](https://ecifre.ro)**
