# Data Sources

This document lists the official institutions eCifre draws data from, as reflected in eCifre's own source registry (`GET /api/v1/sources` on the eCifre API), and states which of them are represented in this repository's `datasets/` folder.

| Source | Institution | URL | Type | Notes |
| --- | --- | --- | --- | --- |
| ANCOM | Autoritatea Națională pentru Administrare și Reglementare în Comunicații | https://sscpds.ancom.ro | Regulator | Public data |
| ANOFM | Agenția Națională pentru Ocuparea Forței de Muncă | https://www.anofm.ro | Public agency | Public data |
| ANRE_GAS | Autoritatea Națională de Reglementare în Domeniul Energiei | https://anre.ro | Regulator | Public data |
| ASF | Autoritatea de Supraveghere Financiară | https://asfromania.ro | Regulator | Public data |
| ASF_INSURANCE | Autoritatea de Supraveghere Financiară — piața asigurărilor | https://asfromania.ro | Regulator | Public data |
| BNR | Banca Națională a României | https://www.bnr.ro | Central bank | Public data |
| **BVB** | Bursa de Valori București | https://bvb.ro | Stock exchange | **Restrictive license** — redistribution/public display requires written consent (see bvb.ro/Disclaimer.aspx). **Not included in this repository.** |
| CNP | Comisia Națională de Strategie și Prognoză | https://cnp.ro | Public agency | Public data (forecasts) |
| CNPP | Casa Națională de Pensii Publice | https://www.cnpp.ro | Public agency | Public data |
| **DATAGOV** | data.gov.ro | https://data.gov.ro | Open data portal | License varies per dataset (CKAN platform) — each resource must be checked individually. **Not included in this repository** until reviewed per-dataset. |
| ECB | European Central Bank | https://data.ecb.europa.eu | Central bank | ECB Data Portal — free reuse with attribution |
| ECIFRE | eCifre (calculated) | — | Derived | Indicators calculated by eCifre from other public indicators, not sourced directly from an external institution. Calculation methodology is documented per indicator. |
| ENTSOE | ENTSO-E Transparency Platform | https://web-api.tp.entsoe.eu/api | International organization | Reuse per EU Regulation 543/2013 |
| EUROSTAT | Eurostat | https://ec.europa.eu/eurostat | EU statistical office | © European Union, 1995 – today |
| INSSE | Institutul Național de Statistică | https://insse.ro | National statistics office | Public data |
| MFIN | Ministerul Finanțelor | https://mfinante.gov.ro | Ministry | Public data |
| MONITORULPRETURILOR | Monitorul Prețurilor (Consiliul Concurenței + ANPC) | https://monitorulpreturilor.info | Public platform | Platform states prices shown are public and current; no scraping/republishing restriction found |
| ONRC | Oficiul Național al Registrului Comerțului | https://www.onrc.ro | Public registry | Public data |
| **OPCOM** | OPCOM | https://www.opcom.ro | Power exchange | **Restrictive license** — internal use only, no public exposure without written consent (see opcom.ro/disclaimer/133/ro). **Not included in this repository.** |
| TRANSELECTRICA | Transelectrica (Sistemul Energetic Național) | https://www.transelectrica.ro | Grid operator | Public, unrestricted data |
| WORLDBANK | World Bank | https://api.worldbank.org | International organization | CC BY-4.0 |

## Sources excluded from this repository

Two sources carry explicit redistribution restrictions in their own published terms, and are excluded from every dataset here even though eCifre.ro may display them (with live fetching itself gated behind an explicit license-confirmation flag in eCifre's own configuration):

- **BVB** (Bursa de Valori București) — requires written consent for redistribution or public display.
- **OPCOM** — internal use only; no public exposure without written consent.

**DATAGOV** (data.gov.ro) is also excluded for now, since its license varies per individual dataset (CKAN platform) and each resource would need to be checked before republishing.

If you need data from one of these sources, use the linked website directly.
