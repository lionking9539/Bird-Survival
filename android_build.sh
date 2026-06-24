#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install buildozer

echo "Android packaging prerequisites are installed."
echo "Next, install the Android SDK/NDK and run one of these commands:"
echo "  buildozer -v android debug"
echo "  buildozer -v android release"
