#!/usr/bin/env bash
# Acceptance smoke test for M2-04: DVC metadata must restore raw project data.
set -euo pipefail

required_paths=(
  "raw-fer2013.dvc"
  "raw-persona.dvc"
)

for path in "${required_paths[@]}"; do
  test -f "$path" || { echo "missing DVC metadata: $path" >&2; exit 1; }
done

test "$(dvc config core.remote)" = "mirror_gcs"
test "$(dvc config remote.mirror_gcs.url)" = "gs://mirror-ac215-data/dvc"

dvc pull --quiet

test -s data/raw/fer2013/archive.zip
test -s data/raw/persona/jbp_clean_full.csv
test -s data/raw/persona/jbp_train.csv
test -s data/raw/persona/jbp_val.csv
test -s data/raw/persona/jbp_test.csv

echo "M2-04 DVC smoke test passed"
