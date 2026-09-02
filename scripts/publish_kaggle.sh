#!/usr/bin/env bash
# Build, validate, and publish the eCifre Kaggle dataset.
#
# Requires the Kaggle CLI to already be installed and authenticated in this
# environment (either ~/.kaggle/kaggle.json, or KAGGLE_USERNAME + KAGGLE_KEY
# environment variables). This script never reads or writes credentials
# itself — see kaggle/README.md and the repository README for setup.
#
# Usage:
#   scripts/publish_kaggle.sh create              # first-ever publish
#   scripts/publish_kaggle.sh version "message"    # publish a new version of an existing dataset
#
# Both modes build + validate first and abort on any failure, including the
# deliberate placeholders left in kaggle/dataset-metadata.json (owner slug,
# license) until you've replaced them for real.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
METADATA_FILE="$REPO_ROOT/kaggle/dataset-metadata.json"
BUILD_FILE="$REPO_ROOT/kaggle/build/romania_economic_indicators.csv"

mode="${1:-}"
if [[ "$mode" != "create" && "$mode" != "version" ]]; then
  echo "Usage: $0 create | version \"version message\"" >&2
  exit 1
fi

if [[ "$mode" == "version" && -z "${2:-}" ]]; then
  echo "A version message is required: $0 version \"what changed\"" >&2
  exit 1
fi

if ! command -v kaggle >/dev/null 2>&1; then
  echo "ERROR: the 'kaggle' CLI is not installed. Install it with: pip install kaggle" >&2
  exit 1
fi

if [[ -z "${KAGGLE_USERNAME:-}${KAGGLE_KEY:-}" && ! -f "$HOME/.kaggle/kaggle.json" ]]; then
  echo "ERROR: no Kaggle credentials found (no \$HOME/.kaggle/kaggle.json and no" >&2
  echo "KAGGLE_USERNAME/KAGGLE_KEY environment variables). See kaggle/README.md." >&2
  exit 1
fi

if grep -q "REPLACE_WITH_KAGGLE_OWNER_SLUG" "$METADATA_FILE"; then
  echo "ERROR: kaggle/dataset-metadata.json still has the placeholder owner slug." >&2
  echo "Replace \"id\" with the real \"<kaggle-owner>/romania-economic-indicators\" first." >&2
  exit 1
fi

if grep -q "DECISION-NEEDED" "$METADATA_FILE"; then
  echo "ERROR: kaggle/dataset-metadata.json still has the license placeholder." >&2
  echo "See kaggle/LICENSE_NOTES.md — a license must be decided before publishing." >&2
  exit 1
fi

echo "== Build =="
python3 "$REPO_ROOT/scripts/build_kaggle_dataset.py"

echo
echo "== Validate =="
python3 "$REPO_ROOT/scripts/validate_dataset.py" "$BUILD_FILE"

echo
echo "== Publish ($mode) =="
if [[ "$mode" == "create" ]]; then
  kaggle datasets create -p "$REPO_ROOT/kaggle" --dir-mode zip
else
  kaggle datasets version -p "$REPO_ROOT/kaggle" --dir-mode zip -m "$2"
fi

echo
echo "Done."
