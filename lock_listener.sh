#!/bin/bash

# Path to your state update script
UPDATE_SCRIPT="$HOME/Projects/small_scripts/update_lock_state.sh"

# Listen to the system bus for screen saver state changes
gdbus monitor -y -d org.freedesktop.login1 | grep --line-buffered "LockedHint" | while read -r line; do
    if echo "$line" | grep -q "true"; then
        # The system natively broadcasted that it locked
        "$UPDATE_SCRIPT" lock
    elif echo "$line" | grep -q "false"; then
        # The system natively broadcasted that it unlocked
        "$UPDATE_SCRIPT" unlock
    fi
done
