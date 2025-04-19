# Screenshot Capture & PDF Builder

Automates capturing full‑page screenshots of a Qualtrics survey, trimming them, and optionally bundling them into a single PDF.

---

## Prerequisites

- **Python 3.9+** (the project is tested with Python 3; use `python` or `python3` as available)
- Google Chrome (or Chromium) installed, with a matching ChromeDriver
- `git`, `bash`, and typical build tools available on macOS or Linux

---

## Quick Start

```bash

# 0 Create a file called .env
# Add the public URL of your Qualtrics survey in there, like this:
# QUALTRICS_URL=https://umich.qualtrics.com/jfe/form/SV_xxxxxxxxxxx
# Make sure this survey has no validation or force response requirements

# 1 Create & activate a virtual environment
python3 -m venv .venv      # use `python` if that's your default interpreter
source .venv/bin/activate  # zsh/bash; Windows PowerShell: .venv\\Scripts\\Activate.ps1

# 2 Install dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# 3 Run the bash script
./run_all.sh

# 4 Combine the png files in the screenshots_trimmed/ folder into a pdf
# (check images first and do manual cropping if needed)
./combine_to_pdf.sh
```

run_all.sh will:

1. Launch Chrome via Selenium.

2. Capture full‑page screenshots into screenshots/.

3. Trim the images and save them to screenshots_trimmed/.
