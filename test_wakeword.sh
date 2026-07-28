#!/bin/bash

# Project directory
PROJECT_DIR="/home/kida-01/Desktop/Kida-Robot"
cd "$PROJECT_DIR"

# Activate virtual environment if present
if [ -d "venv" ]; then
    source venv/bin/activate
fi

mkdir -p "$PROJECT_DIR/logs"
LOG_FILE="$PROJECT_DIR/logs/wakeword_test.log"
export HAILORT_LOGGER_PATH="$PROJECT_DIR/logs"

echo "Starting kida_chat_wakeword.py at $(date)" | tee -a "$LOG_FILE"
python3 -u scripts/kida_chat_wakeword.py 2>&1 | tee -a "$LOG_FILE"
