# Romania Economic Indicators — eCifre

## Overview

A structured and versioned collection of economic indicators for Romania, compiled and normalized by **[eCifre](https://ecifre.ro)** from official Romanian and European public data sources.

This Zenodo record is a versioned snapshot of eCifre's public economic dataset. eCifre's own pipeline — not Zenodo — remains the live, continuously-updated source; each Zenodo version captures the dataset's state at a point in time, for permanent, citable reference.

Interactive visualizations, current values, indicator methodology and economic context are available at **https://ecifre.ro**.

## Dataset contents

| File | Description |
| --- | --- |
| `romania_economic_indicators.csv` | The full dataset, comma-separated, UTF-8 |
| `romania_economic_indicators.parquet` | Same data, Parquet format (typed columns, smaller, faster to load) |
| `README.md` | This file |
| `DATA_DICTIONARY.md` | Column-by-column reference |
| `DATA_SOURCES.md` | Full list of institutions eCifre draws from, with licensing notes |
| `CHANGELOG.md` | What changed in each release |
| `CITATION.cff` | Machine-readable citation metadata |
| `SHA256SUMS` | Checksums for the two data files, for integrity verification |

## Data structure

One row per (indicator, geography, date) observation.

| Column | Description |
| --- | --- |
| `indicator` | Human-readable indicator name, in Romanian |
| `indicator_slug` | Stable eCifre identifier (e.g. `inflatie-anuala-ro`) |
| `date` | Observation / reference period (ISO 8601) |
| `value` | Observed value, exactly as published by the source |
| `unit` | Unit of measurement |
| `geography` | `Romania` for national indicators, or a county name for county-level indicators |
| `frequency` | `daily`, `monthly`, `quarterly`, `annual`, or `irregular` |
| `source` | Original data provider's short code |
| `source_url` | Link to the original source |
| `ecifre_url` | Link to the indicator's page on eCifre — interactive chart, methodology, context |
| `last_updated` | Date eCifre's pipeline last successfully refreshed this indicator |

Full reference: `DATA_DICTIONARY.md`.

## Sources

Data is derived from official institutions actually represented in this release — see `DATA_SOURCES.md` for the complete list with licensing notes for each.

## Methodology

eCifre normalizes data from these different official sources to improve consistency across naming, dates, units, geographic entities, frequencies and historical time series. Each indicator keeps the definition and calculation method used by its original source — eCifre does not re-derive or re-estimate published figures.

Detailed, per-indicator methodology: **https://ecifre.ro/indicatori**

## Geographic coverage

National-level Romania, plus all 42 counties (județe) including București, for the indicators that are tracked at county level.

## Temporal coverage

Varies by indicator — see `CHANGELOG.md` for this release's exact date range, and `last_updated` per row for how current each series is.

## Update frequency

eCifre's live pipeline refreshes continuously; this Zenodo record is versioned on a roughly monthly cadence (calendar versioning, e.g. `2026.09`), and only when the underlying data has actually changed since the last version.

## Limitations

- Source institutions publish on different schedules and sometimes revise historical values after initial publication.
- Methodology can differ between sources measuring related concepts (e.g. ILO/BIM unemployment vs. registered unemployment) — check `source` and `ecifre_url` before comparing across indicators.
- Not every indicator shares the same geographic or frequency coverage.
- A few indicators currently have very short histories because that's genuinely all the source institution has published so far.
- **eCifre is not the original statistical authority for any of this data.** The institutions listed in `DATA_SOURCES.md` remain authoritative for their respective figures; eCifre collects, normalizes and republishes what they publish.

## Citation

See `CITATION.cff` for machine-readable metadata, or `CITATION.md` in the [source repository](https://github.com/eCifre/romania-economic-data) for plain-text/APA/BibTeX formats.

## About eCifre

eCifre is a Romanian platform for discovering, visualizing and understanding official economic data: **https://ecifre.ro**
