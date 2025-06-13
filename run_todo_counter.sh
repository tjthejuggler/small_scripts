#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
  source ./.venv/bin/activate
fi

# Run the Python script
python3 /home/twain/Projects/small_scripts/todoCounter-increase.py