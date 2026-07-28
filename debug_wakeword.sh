#!/bin/bash

# Project directory
PROJECT_DIR="/home/kida-01/Desktop/Kida-Robot"
cd "$PROJECT_DIR"

# Activate virtual environment if present
if [ -d "venv" ]; then
    source venv/bin/activate
fi

mkdir -p "$PROJECT_DIR/logs"
export HAILORT_LOGGER_PATH="$PROJECT_DIR/logs"

python3 scripts/debug_wakeword.py
