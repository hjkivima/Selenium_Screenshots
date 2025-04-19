#!/usr/bin/env python3
# trim.py  –  batch‑crop screenshots as specified

from pathlib import Path
import numpy as np
from PIL import Image

# ---- parameters you asked for ------------------------------------------------
TARGET_WIDTH = 800  # px
WHITE_THRESHOLD = 245  # R,G,B values above this count as “white”
MIN_WHITE_RUN = 300  # px of white before we intervene
KEEP_WHITE_MARGIN = 20  # px of white to keep

# ---- folders -----------------------------------------------------------------
SRC_DIR = Path(__file__).parent / "screenshots"
DEST_DIR = Path(__file__).parent / "screenshots_trimmed"


# ------------------------------------------------------------------------------
def is_row_white(row: np.ndarray) -> bool:
    """True if every pixel in the row is nearly white."""
    return (row > WHITE_THRESHOLD).all(axis=1).all()


def crop_image(img: Image.Image) -> Image.Image:
    """Apply width‑crop and bottom‑whitespace trim."""
    w, h = img.size

    # 1) centre‑crop to 800 px width
    if w > TARGET_WIDTH:
        left = (w - TARGET_WIDTH) // 2
        img = img.crop((left, 0, left + TARGET_WIDTH, h))
        w = TARGET_WIDTH

    # 2) trim bottom white run
    arr = np.asarray(img)  # (h, w, 3) array
    white_run = 0
    for row in arr[::-1]:  # scan from bottom upward
        if is_row_white(row):
            white_run += 1
        else:
            break

    if white_run > MIN_WHITE_RUN:
        new_h = h - white_run + KEEP_WHITE_MARGIN
        img = img.crop((0, 0, w, new_h))

    return img


def main() -> None:
    if not SRC_DIR.is_dir():
        raise SystemExit(f"folder not found: {SRC_DIR}")

    DEST_DIR.mkdir(exist_ok=True)

    pngs = sorted(SRC_DIR.glob("*.png"))
    if not pngs:
        raise SystemExit(f"no PNGs found in {SRC_DIR}")

    for path in pngs:
        try:
            img = Image.open(path).convert("RGB")
            out = crop_image(img)
            out.save(DEST_DIR / path.name)
            print(f"✔ {path.name}  →  {out.width}×{out.height}px")
        except Exception as e:
            print(f"✘ {path.name}: {e}")


if __name__ == "__main__":
    main()
