# License decision needed before publishing to Kaggle

Kaggle requires every dataset to declare a license in `dataset-metadata.json`. `romania_economic_indicators.csv` aggregates data from **8 different institutions**, and their own published terms are not uniform — so a single license cannot be picked automatically without either overstating or understating what we're actually allowed to grant. This file exists so that decision is made deliberately, not by default.

The current `dataset-metadata.json` has `licenses[0].name` set to the placeholder string `"DECISION-NEEDED-see-kaggle/LICENSE_NOTES.md"`, which is **not a valid Kaggle license identifier on purpose** — `kaggle datasets create`/`version` will reject it until it's replaced with a real choice. That's intentional: it blocks an accidental publish with the wrong license.

## Sources actually present in this dataset

| Source | Institution | Stated terms |
| --- | --- | --- |
| INSSE | Institutul Național de Statistică | "Date publice" — publicly published, but INSSE does not state an explicit open-reuse license (no CC mark found) |
| BNR | Banca Națională a României | "Date publice" — same: public, no explicit reuse license stated |
| MFIN | Ministerul Finanțelor | "Date publice" — same |
| ANOFM | Agenția Națională pentru Ocuparea Forței de Muncă | "Date publice" — same |
| ANRE_GAS | Autoritatea Națională de Reglementare în Domeniul Energiei | "Date publice" — same |
| ONRC | Oficiul Național al Registrului Comerțului | "Date publice" — same |
| EUROSTAT | Eurostat | © European Union, 1995 – today. Eurostat's standard reuse policy (Commission Decision 2011/833/EU) permits free reuse, including commercially, with attribution — functionally close to CC BY 4.0, but Eurostat states its own policy rather than applying the CC BY label itself |
| ENTSOE | ENTSO-E Transparency Platform | Reuse permitted under EU Regulation 543/2013 (the regulation that mandates the platform's data be public) |

None of these sources are BVB or OPCOM (which carry explicit written-consent-required restrictions — see the main [DATA_SOURCES.md](../DATA_SOURCES.md)), so nothing in this specific export is under a known restrictive license. But "not restrictive" is not the same as "we can apply CC0" — several sources (INSSE, BNR, MFIN, ANOFM, ANRE_GAS, ONRC) simply don't state a reuse license at all.

## Options, with tradeoffs

1. **"Other (specified in description)"** (Kaggle supports this) — describe the mixed provenance in the dataset description/README instead of picking a single CC-style label. Safest option; doesn't assert a right we haven't confirmed. Slightly less convenient for downstream users who filter by license on Kaggle.
2. **CC BY 4.0** — reasonably defensible for the Eurostat/ENTSO-E portion (both effectively permit this), and arguably fine for eCifre's own normalization/structuring work on top of the "date publice" sources, but this would be **asserting** an open license on INSSE/BNR/MFIN/ANOFM/ANRE_GAS/ONRC data that those institutions themselves haven't explicitly granted.
3. **Contact each Romanian institution to confirm reuse terms**, then apply the confirmed license. Most correct, slowest.

## Recommendation

Option 1 ("Other", with the source-by-source table above in the dataset description) is the option that doesn't require asserting anything we can't back up. If you'd rather move faster with option 2, that's a judgment call I'd rather you make explicitly than have it applied silently — happy to update `dataset-metadata.json` and the README once you've decided.

**Once decided:** replace `"DECISION-NEEDED-see-kaggle/LICENSE_NOTES.md"` in `kaggle/dataset-metadata.json` with the real Kaggle license identifier (e.g. `"CC-BY-4.0"`, `"other"`, `"unknown"` — see `kaggle datasets list --licenses` or the [Kaggle license list](https://github.com/Kaggle/kaggle-api/blob/main/KaggleDatasetsSchema.json) for the accepted values).
