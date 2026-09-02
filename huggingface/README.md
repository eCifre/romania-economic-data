---
pretty_name: Romania Economic Indicators
language:
- en
- ro
license: other
license_name: mixed-sources-see-license-file
tags:
- economics
- romania
- economic-data
- statistics
- time-series
- gdp
- inflation
- unemployment
- wages
- finance
- open-data
- tabular
configs:
- config_name: default
  data_files:
  - split: train
    path: "data/romania_economic_indicators.parquet"
  default: true
---

# Romania Economic Indicators

**Romania Economic Indicators** is a structured collection of historical economic data for Romania, compiled and normalized by **[eCifre](https://ecifre.ro)** from official Romanian and European public sources.

eCifre makes Romanian economic data easier to discover, understand and compare.

Interactive charts, latest values, methodology and economic context: **https://ecifre.ro**

## Dataset overview

The dataset contains historical time series covering:

- GDP and economic growth
- inflation
- wages and salaries
- employment and unemployment
- exchange rates
- public finance (budget revenue/expenditure, deficit, public debt)
- construction (cost index, building permits, completed dwellings)
- energy (natural gas and electricity consumption/production/prices)
- population and demographics
- county-level (regional) indicators for all 42 Romanian counties plus București

This is a subset of eCifre's full catalog (500+ indicators) — a representative starting set spanning 28 indicators, not everything eCifre tracks.

## Data structure

One row per (indicator, geography, date) observation, sorted by `indicator_slug`, `geography`, then `date`.

| Column | Description |
| --- | --- |
| `indicator` | Human-readable indicator name, in Romanian |
| `indicator_slug` | Stable eCifre identifier (e.g. `inflatie-anuala-ro`) |
| `date` | Observation / reference period |
| `value` | Observed value, exactly as published by the source |
| `unit` | Unit of measurement |
| `geography` | `Romania` for national indicators, or a county name (ASCII, e.g. `Cluj`, `Timis`) for county-level indicators |
| `frequency` | `daily`, `monthly`, `quarterly`, `annual`, or `irregular` |
| `source` | Original data provider's short code (e.g. `INSSE`, `BNR`) |
| `source_url` | Link to the original source |
| `ecifre_url` | Link to the indicator's page on eCifre — interactive chart, methodology, context |
| `last_updated` | Date eCifre's pipeline last successfully refreshed this indicator |

Full column reference: [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

There are no null/blank cells — every row is a real, source-published value. If a period has no published value, that period simply has no row (so a series is not guaranteed to be perfectly regular).

## Data sources

Data is derived from official institutions actually represented in this dataset:

- **Institutul Național de Statistică (INSSE)**
- **Banca Națională a României (BNR)**
- **Eurostat**
- **Ministerul Finanțelor (MFIN)**
- **Agenția Națională pentru Ocuparea Forței de Muncă (ANOFM)**
- **ANRE** — natural gas market data
- **ENTSO-E Transparency Platform** — European electricity market data
- **Oficiul Național al Registrului Comerțului (ONRC)**

## Methodology

eCifre normalizes data from these different official sources to improve consistency across naming, dates, units, geographic entities, frequencies and historical time series. Each indicator keeps the definition and calculation method used by its original source — eCifre does not re-derive or re-estimate published figures.

Detailed, per-indicator methodology: **https://ecifre.ro/indicatori**

## Use cases

- economic research
- journalism
- data science and data visualization
- education
- economic analysis
- AI / machine learning, retrieval-augmented generation (RAG), and other LLM applications working with Romanian economic data

## Limitations

- Source institutions publish on different schedules and sometimes revise historical values after initial publication — a value pulled today may differ slightly from the same period pulled later, if the source itself revised it.
- Methodology can differ between sources measuring related concepts (e.g. ILO/BIM unemployment vs. registered unemployment) — check `source` and the indicator's `ecifre_url` before comparing across indicators.
- Not every indicator has the same geographic or frequency coverage; some are national-only, others are county-level; some are daily, others annual.
- A few indicators currently have very short histories (occasionally a single observation) because that's genuinely all the source institution has published so far — not a loading error.
- **eCifre is not the original statistical authority for any of this data.** The institutions listed above remain the authoritative source for their respective figures; eCifre collects, normalizes and republishes what they publish.

## Programmatic usage

```python
from datasets import load_dataset

dataset = load_dataset("ecifre/romania-economic-indicators")
print(dataset)
```

Filtering to a single indicator:

```python
inflation = dataset["train"].filter(lambda row: row["indicator_slug"] == "inflatie-anuala-ro")
print(inflation.to_pandas().tail())
```

## Attribution

**eCifre — Romania Economic Indicators**
https://ecifre.ro

## Citation

This dataset has a permanent, versioned snapshot on Zenodo with a DOI. If you use this dataset, please cite:

> eCifre. Romania Economic Indicators. Zenodo. https://doi.org/10.5281/zenodo.22255140

The DOI above is the concept DOI (always resolves to the latest version); see [CITATION.md](https://github.com/eCifre/romania-economic-data/blob/main/CITATION.md) in the source repository for the versioned DOI, APA and BibTeX formats.

## License

See [LICENSE](LICENSE) — this dataset aggregates 8 institutions whose own publication terms are not uniform, so no single standard license (CC0, CC-BY, etc.) is asserted. Full reasoning: [LICENSE_NOTES.md](https://github.com/eCifre/romania-economic-data/blob/main/LICENSE_NOTES.md) in the source repository.

## About eCifre

eCifre is a Romanian platform for discovering, visualizing and understanding official economic data.

https://ecifre.ro
