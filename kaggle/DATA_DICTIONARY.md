# Data Dictionary

Columns in `build/romania_economic_indicators.csv`.

| Column | Type | Description |
| --- | --- | --- |
| `indicator` | string | Human-readable indicator name, in Romanian (e.g. `Inflație anuală (România)`) |
| `indicator_slug` | string | Stable eCifre identifier for the indicator (e.g. `inflatie-anuala-ro`); the same value used in the indicator's `ecifre_url` |
| `date` | date (`YYYY-MM-DD`) | Observation / reference period, ISO 8601 |
| `value` | number | Observed value for that period, exactly as published by the source (no rounding beyond what the source itself publishes) |
| `unit` | string | Unit of measurement (e.g. `Lei`, `%`, `RON`, `Milioane lei`) |
| `geography` | string | `Romania` for national-level indicators, or a Romanian county name (ASCII, diacritics removed — e.g. `Cluj`, `Timis`, `Bucuresti`) for county-level indicators |
| `frequency` | string | `daily`, `monthly`, `quarterly`, `annual`, or `irregular` |
| `source` | string | Source institution's short code (e.g. `INSSE`, `BNR`, `EUROSTAT`) — see [README.md](README.md#sources) for full names |
| `source_url` | string | The source institution's website |
| `ecifre_url` | string | The indicator's page on eCifre — includes interactive chart, methodology and context |
| `last_updated` | date (`YYYY-MM-DD`) | Date eCifre's pipeline last successfully refreshed this indicator from its source |

## Notes

- **Missing values:** there are no null/blank cells in this dataset — every row has a real, source-published value. If a period has no published value for an indicator, that period simply has no row (rather than a blank one). This means a time series is not guaranteed to be perfectly regular (e.g. a monthly series may have gaps where the source itself didn't publish that month).
- **`value` precision:** kept exactly as returned by eCifre's API (typically 4 decimal places for most series), not re-rounded.
- **Encoding:** UTF-8. `indicator` and `unit` may contain Romanian diacritics (ă, â, î, ș, ț); `geography` deliberately does not (see above).
- **Delimiter:** standard comma (`,`), with double-quote (`"`) field quoting for any value containing a comma (e.g. indicator names with a parenthetical like `PIB per capita (România, volum înlănțuit)`).
