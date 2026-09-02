# Hugging Face organization card — manual step

Hugging Face organization profile pages work differently from GitHub's: there's no
API-creatable "profile repo". The card is a `README.md` inside a **public Space**
named exactly `README`, owned by the organization (docs:
https://huggingface.co/docs/hub/en/organizations-cards). Space creation isn't
part of `scripts/publish_huggingface.py` (that script only manages the dataset
repo) — this is a one-time manual step, same category as creating the
organization itself.

## Steps

1. Create the organization at https://huggingface.co/organizations/new (Name:
   `eCifre`, matching the requested `ecifre` handle if available).
2. In organization Settings, set:
   - Website: `https://ecifre.ro`
   - Short description: `Romanian economic data, indicators and insights.`
3. On the organization's main page, use the button to create the organization
   card. This creates a public Space named `README` under the org.
4. Replace that Space's `README.md` with the content below.

## Card content

```markdown
# eCifre

**Romania's economy, explained through data.**

eCifre aggregates, normalizes and explains economic data published by official Romanian and European institutions.

Explore economic indicators, historical data, comparisons and interactive charts:

https://ecifre.ro

## Dataset

[Romania Economic Indicators](https://huggingface.co/datasets/ecifre/romania-economic-indicators)
```
