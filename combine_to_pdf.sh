#!/usr/bin/env bash
# combine_to_pdf.sh  –  lossless PNG‑>PDF without using mapfile/readarray
#
#   ./combine_to_pdf.sh                 # defaults
#   ./combine_to_pdf.sh input_dir out.pdf
#
# Dependency:  img2pdf   (pip install img2pdf)

set -euo pipefail

SRC_DIR="${1:-screenshots_trimmed}"
OUT_PDF="${2:-screenshots_trimmed.pdf}"

command -v img2pdf >/dev/null 2>&1 || {
    echo "img2pdf not found.  Install with:  pip install img2pdf" >&2
    exit 1
}

[ -d "$SRC_DIR" ] || {
    echo "Folder not found: $SRC_DIR" >&2
    exit 1
}

# ---- collect PNG paths in ‘natural’ order -----------------------------------
# BSD ls (macOS) supports -v  →  sorts  file2.png  before  file10.png
png_list=$(ls -1v "$SRC_DIR"/*.png 2>/dev/null) || true

[ -n "$png_list" ] || {
    echo "No PNG files in $SRC_DIR" >&2
    exit 1
}

# ---- build the PDF (lossless) -----------------------------------------------
# shell‑word‑splitting on purpose – filenames with spaces will break;
# if you *do* have such names, move to Option B below.
img2pdf $png_list -o "$OUT_PDF"

echo "✔  $(echo "$png_list" | wc -l | tr -d ' ') pages  →  $OUT_PDF"
