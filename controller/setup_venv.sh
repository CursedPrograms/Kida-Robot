#!/bin/bash
# setup_venv.sh — one-time setup for the KIDA remote controller
#
# Creates a venv scoped to scripts/controller only, isolated from the
# robot's own venv/requirements.txt (which pulls in picamera2, RPi.GPIO,
# ultralytics, etc. that don't belong on a plain PC).

set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Controller venv ready. Run with:"
echo "   source $HERE/venv/bin/activate"
echo "   python3 $HERE/main.py <robot-ip>"
