#!/usr/bin/env bash
# -------------------------------------------------------------------
# run_all.sh  – master pipeline
#
#   0. Wipe old artifacts:
#        screenshots/          (raw screenshots)
#        screenshots_trimmed/  (cropped screenshots)
#   1. python3 main.py         (re‑creates screenshots/)
#   2. python3 trim.py         (writes screenshots_trimmed/)
#   3. bash   combine_to_pdf.sh  (combines trimmed PNGs → lossless PDF)
#
# The script aborts on the first error.
# -------------------------------------------------------------------

set -euo pipefail # fail‑fast & treat unset vars as errors

# --- clean slate --------------------------------------------------------------
echo "🗑  Removing old screenshot directories (if present)..."
rm -rf screenshots screenshots_trimmed

# --- re‑generate everything ---------------------------------------------------
echo "▶  Running get_screenshots.py ..."
python3 get_screenshots.py

echo "▶  Trimming screenshots ..."
python3 trim.py

# Better to check the screenshots before combining, so I'm commenting this out
# echo "▶  Combining PNGs into lossless PDF ..."
# bash combine_to_pdf.sh

echo "✅  All steps completed successfully."
