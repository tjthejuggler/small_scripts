#!/bin/bash

# Startup script for File Finder Tray application

# Set script directory as absolute path
SCRIPT_DIR="/home/twain/Projects/small_scripts"
LOG_FILE="$HOME/.local/share/file-finder-tray/startup.log"
VENV_PATH="$SCRIPT_DIR/venv"
APP_PATH="$SCRIPT_DIR/file_finder_tray.py"

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Function for logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Clear log file if it's larger than 1MB
if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE") -gt 1048576 ]; then
    echo "# Log file cleared $(date)" > "$LOG_FILE"
fi

log "Starting File Finder Tray application..."

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    log "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Check if application file exists
if [ ! -f "$APP_PATH" ]; then
    log "Error: Application file not found at $APP_PATH"
    exit 1
fi

# Activate virtual environment and run application
source "$VENV_PATH/bin/activate" 2>> "$LOG_FILE" && \
python3 "$APP_PATH" 2>> "$LOG_FILE"

# Log any errors
if [ $? -ne 0 ]; then
    log "Error: Application failed to start"
    exit 1
fi

exit 0