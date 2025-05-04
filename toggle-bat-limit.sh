#!/bin/bash
# File: toggle-bat-limit.sh
# This script toggles battery limiting modes for your Zenbook Duo.
# Modes (in cycle order):
#   75% (default at startup)
#   50%
#   100% (full charge)
#
# Requires passwordless sudo for the duo command.
# Ensure your sudoers file (via sudo visudo) contains:
#   twain ALL=(ALL) NOPASSWD: /home/twain/Projects/zenbook-duo-2024-ux8406ma-linux/duo

# Path to the duo command
DUO="/home/twain/Projects/zenbook-duo-2024-ux8406ma-linux/duo"

# Define the cycle of battery thresholds.
# In this order: 75, 50, then 100.
states=(75 50 100)
state_names=("75%" "50%" "100%")

num_states=${#states[@]}

# File to store current state index
STATE_FILE="/tmp/duo_bat_limit_state"

# On first run after boot, default to index 0 (75%).
if [ -f "$STATE_FILE" ]; then
    current_index=$(cat "$STATE_FILE")
else
    current_index=0
fi

# Get the current threshold value.
current_state=${states[$current_index]}

# Apply the battery limit using duo.
sudo "$DUO" bat-limit "$current_state"

# Send a KDE notification with the current mode.
notify-send "Battery Limiting Set" "Battery charge threshold set to ${state_names[$current_index]}."

# Cycle to the next state.
next_index=$(( (current_index + 1) % num_states ))
echo "$next_index" > "$STATE_FILE"
