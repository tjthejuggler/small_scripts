#!/bin/bash
# File: cycle-backlight.sh

# File to store the current brightness level
STATE_FILE="/tmp/duo_brightness_state"

# Maximum brightness level (0, 1, 2, 3)
MAX_LEVEL=3

# Read the current brightness level; default to 0 if file doesn't exist
if [ -f "$STATE_FILE" ]; then
    CURRENT=$(cat "$STATE_FILE")
else
    CURRENT=0
fi

# Calculate next brightness level (wraps around from MAX_LEVEL back to 0)
NEXT=$(( (CURRENT + 1) % (MAX_LEVEL + 1) ))

# Save the new brightness level
echo "$NEXT" > "$STATE_FILE"

# Execute the duo command with sudo using its absolute path
sudo /home/twain/Projects/zenbook-duo-2024-ux8406ma-linux/duo set-kb-backlight "$NEXT"
