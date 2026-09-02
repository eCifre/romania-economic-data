# License decision — resolved 2026-09-02

Both Kaggle and Hugging Face require every dataset to declare a license in its metadata. `romania_economic_indicators.csv` aggregates data from **8 different institutions**, and their own published terms are not uniform — so a single license couldn't be picked automatically without either overstating or understating what we're actually allowed to grant. This file documents the analysis and the decision that was made deliberately, not by default. It applies identically on both platforms — the license is not chosen independently per platform.

**Decision: `"other"`** on both platforms, with the source-by-source breakdown below reproduced in full:
- Kaggle: `kaggle/dataset-metadata.json`'s `licenses[0].name` is `"other"`, with the breakdown in its `description` field (Kaggle's own guidance for "Other" is to spell out the actual terms in the description).
- Hugging Face: the dataset card's `license: other` + `license_name`, with the breakdown reproduced in a `LICENSE` file in the Hugging Face repo (required by Hugging Face whenever `license: other` is used).

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

None of these sources are BVB or OPCOM (which carry explicit written-consent-required restrictions — see the main [DATA_SOURCES.md](DATA_SOURCES.md)), so nothing in this specific export is under a known restrictive license. But "not restrictive" is not the same as "we can apply CC0" — several sources (INSSE, BNR, MFIN, ANOFM, ANRE_GAS, ONRC) simply don't state a reuse license at all.

## Options, with tradeoffs

1. **"Other" (terms spelled out in the description/LICENSE, not a CC-style label)** — both Kaggle and Hugging Face support this explicitly. Safest option; doesn't assert a right we haven't confirmed. Slightly less convenient for downstream users who filter by license.
2. **CC BY 4.0** — reasonably defensible for the Eurostat/ENTSO-E portion (both effectively permit this), and arguably fine for eCifre's own normalization/structuring work on top of the "date publice" sources, but this would be **asserting** an open license on INSSE/BNR/MFIN/ANOFM/ANRE_GAS/ONRC data that those institutions themselves haven't explicitly granted.
3. **Contact each Romanian institution to confirm reuse terms**, then apply the confirmed license. Most correct, slowest.

## Decision

Option 1 ("Other", with the source-by-source table above reproduced in each platform's own required place — see above) was chosen — it doesn't require asserting a reuse right that INSSE, BNR, MFIN, ANOFM, ANRE_GAS or ONRC haven't explicitly granted. If this ever needs revisiting (e.g. after confirming an explicit license with one of the Romanian institutions, per option 3 above), update it consistently in **both** `kaggle/dataset-metadata.json` and the Hugging Face dataset card / `LICENSE` file — never one without the other.
