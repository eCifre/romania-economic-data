# Romania Economic Data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22255140.svg)](https://doi.org/10.5281/zenodo.22255140)

Open datasets containing economic indicators for Romania.

The datasets are collected, cleaned and normalized by **[eCifre](https://ecifre.ro)**, using data published by official Romanian and European institutions. This repository publishes a subset of that data as plain CSV files for reuse outside the eCifre platform.

Interactive charts, latest values, methodology and economic context for every indicator: **[ecifre.ro](https://ecifre.ro)**

> This repository contains **data only**. The eCifre application (web, API backend, mobile, admin) is closed-source and not published here or anywhere else on GitHub.

## Available data

Datasets are organized by topic under [`datasets/`](datasets/):

| Folder | Contents |
| --- | --- |
| [`inflation/`](datasets/inflation) | Annual and monthly CPI-based inflation |
| [`gdp/`](datasets/gdp) | GDP growth, real and nominal GDP |
| [`wages/`](datasets/wages) | Average gross/net wages, minimum wage |
| [`unemployment/`](datasets/unemployment) | ILO (BIM) and registered unemployment rate |
| [`exchange-rates/`](datasets/exchange-rates) | Daily official EUR/RON rate (BNR) |
| [`public-finance/`](datasets/public-finance) | Public debt, budget revenue/expenditure, budget deficit |
| [`construction/`](datasets/construction) | Construction cost index, building permits, completed dwellings (by county) |
| [`energy/`](datasets/energy) | Natural gas and electricity consumption/production/prices |
| [`population/`](datasets/population) | Resident population and demographic dependency, by county |
| [`counties/`](datasets/counties) | County-level GDP, new business registrations, birth rate |

This is a starting set, not the full eCifre catalog (eCifre tracks 500+ indicators). More datasets may be added over time — see [CONTRIBUTING.md](CONTRIBUTING.md) if you'd like to request one.

## Data sources

Data is derived from official sources such as:

- **Institutul Național de Statistică (INSSE)**
- **Banca Națională a României (BNR)**
- **Eurostat**
- **Ministerul Finanțelor**
- **ANRE**, **ENTSO-E**

The full list of sources eCifre draws from, with licensing notes, is documented in [DATA_SOURCES.md](DATA_SOURCES.md). A small number of sources used elsewhere on eCifre (e.g. Bursa de Valori București, OPCOM) carry redistribution restrictions and are **deliberately excluded** from this repository.

## Schema

Each CSV uses a consistent column layout:

| Column | Description |
| --- | --- |
| `indicator` | Human-readable indicator name |
| `date` | Reference period (ISO 8601, `YYYY-MM-DD`) |
| `value` | The value for that period, as published |
| `unit` | Unit of measurement |
| `geography` | `RO` for national values, or an ISO 3166-2 county code (e.g. `RO-AB`) for county-level data |
| `source` | Source institution code (see [DATA_SOURCES.md](DATA_SOURCES.md)) |
| `source_url` | Source institution's website |
| `ecifre_url` | Link to the indicator's page on eCifre, with chart, methodology and context |
| `last_updated` | Date of the source's last successful data refresh in eCifre |

## Methodology

eCifre standardizes data from different official sources to improve consistency across dates, units, naming conventions, time periods and geographic entities. Each indicator keeps the definition and calculation method used by its original source — eCifre does not re-derive or re-estimate published figures, aside from a small set of indicators explicitly marked as eCifre-calculated (see `ECIFRE` in [DATA_SOURCES.md](DATA_SOURCES.md)).

Detailed, per-indicator methodology notes are available on each indicator's `ecifre_url`, and a growing reference set is being documented in [economic-indicators-romania](https://github.com/eCifre/economic-indicators-romania).

## Beyond GitHub: Kaggle, Hugging Face, Zenodo

The data in `datasets/` is consolidated by a single canonical build ([`scripts/build_canonical_dataset.py`](scripts/build_canonical_dataset.py)) into one sorted, normalized file — [`build/romania_economic_indicators.csv`](build/romania_economic_indicators.csv). Every other distribution platform packages *that same file*; none of them re-derive or re-normalize the data independently:

| Platform | Packaging | Publish script | Status |
| --- | --- | --- | --- |
| [Kaggle](https://www.kaggle.com/datasets/stefanvergu/romania-economic-indicators) | [`kaggle/`](kaggle/) | `scripts/publish_kaggle.sh` | Published |
| [Hugging Face](https://huggingface.co/datasets/ecifre/romania-economic-indicators) | [`huggingface/`](huggingface/) (dataset card + LICENSE; also distributed as Parquet) | `scripts/publish_huggingface.py` | Published |
| [Zenodo](https://doi.org/10.5281/zenodo.22255140) | [`zenodo/`](zenodo/) (versioned, DOI-bearing snapshots — CSV + Parquet + docs + checksums) | `scripts/publish_zenodo.py` | Published — v2026.09, DOI [10.5281/zenodo.22255141](https://doi.org/10.5281/zenodo.22255141) |

`romania_economic_indicators.parquet` is generated from the canonical CSV by [`scripts/csv_to_parquet.py`](scripts/csv_to_parquet.py) — serialization only, no value changes. Schema (11 columns: `indicator`, `indicator_slug`, `date`, `value`, `unit`, `geography`, `frequency`, `source`, `source_url`, `ecifre_url`, `last_updated`), data dictionary, and license reasoning are documented once, at the repo root — [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) and [`LICENSE_NOTES.md`](LICENSE_NOTES.md) — and referenced from each platform folder rather than duplicated. Citation info: [`CITATION.md`](CITATION.md), [`CITATION.cff`](CITATION.cff).

## Licensing

The underlying data is published by Romanian and European public institutions under varying terms — some sources place their data fully in the public domain, others require attribution, and a few are more restrictive. We have **not** applied a blanket license (like CC0 or MIT) to the datasets in this repository, because that would overstate what we can legally grant for every source. See [DATA_SOURCES.md](DATA_SOURCES.md) for source-by-source notes, and check the linked source before redistributing a dataset further.

## Usage

These datasets are intended to be useful for:

- economic research and journalism
- education
- data science and data visualization
- software development
- AI / machine learning training and evaluation
- economic analysis

## Attribution

When using data prepared by eCifre, attribution is appreciated:

**eCifre — Romanian Economic Data** — [ecifre.ro](https://ecifre.ro)

## About eCifre

eCifre makes Romanian economic data easier to discover, understand and compare: **[ecifre.ro](https://ecifre.ro)**
