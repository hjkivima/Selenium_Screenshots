from __future__ import annotations
import base64, time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.environ["QUALTRICS_URL"]  # unchanged

DIR = Path("screenshots")
TIMEOUT = 20
DIR.mkdir(exist_ok=True)


# ─────────────────────────── helpers ─────────────────────────────────────────
def capture_full_page(driver, outfile: Path, base_css_width: int) -> None:
    """Take a full‑page PNG, scaled so pixel width ≤ base_css_width."""
    metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    css_w, css_h = metrics["contentSize"]["width"], metrics["contentSize"]["height"]

    scale = min(1.0, base_css_width / css_w)  # shrink only, never enlarge

    driver.execute_cdp_cmd(
        "Emulation.setDeviceMetricsOverride",
        {
            "mobile": False,
            "width": css_w,
            "height": css_h,
            "deviceScaleFactor": scale,
            "screenOrientation": {"angle": 0, "type": "portraitPrimary"},
        },
    )
    raw = driver.execute_cdp_cmd(
        "Page.captureScreenshot",
        {"fromSurface": True, "captureBeyondViewport": True},
    )["data"]
    outfile.write_bytes(base64.b64decode(raw))
    driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})


def _next_button_if_ready(driver):
    try:
        btn = driver.find_element(By.ID, "NextButton")
    except (NoSuchElementException, StaleElementReferenceException):
        return False

    if (
        not btn.is_displayed()
        or not btn.is_enabled()
        or btn.get_attribute("aria-disabled") == "true"
    ):
        return False
    return btn


def wait_for_next(driver):
    wait = WebDriverWait(
        driver,
        TIMEOUT,
        ignored_exceptions=(
            NoSuchElementException,
            StaleElementReferenceException,
        ),
    )
    try:
        return wait.until(lambda d: _next_button_if_ready(d))
    except TimeoutException:
        return None


# ──────────────────────────── main ───────────────────────────────────────────
def main() -> None:
    driver = webdriver.Chrome()
    driver.get(URL)

    # ── establish baseline width on the *very first* page ────────────────
    first_metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    BASE_CSS_WIDTH = first_metrics["contentSize"]["width"]

    page = 1
    while True:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        path = DIR / f"page{page:02d}_{ts}.png"
        capture_full_page(driver, path, BASE_CSS_WIDTH)
        print(f"[{page}] saved {path.name}")

        nxt = wait_for_next(driver)
        if nxt is None:  # last page
            break

        nxt.click()
        page += 1
        time.sleep(0.5)  # let the new DOM settle

    driver.quit()


if __name__ == "__main__":
    main()
