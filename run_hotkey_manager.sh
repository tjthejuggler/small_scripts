#!/bin/bash
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

export PYTHONUNBUFFERED=1
export DISPLAY="${DISPLAY:-:0}"
python3 /home/twain/Projects/small_scripts/hotkey_manager.py