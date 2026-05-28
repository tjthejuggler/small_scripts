#!/bin/bash
STATE_FILE="$HOME/.pc_lock_state"

if [ "$1" = "lock" ]; then
    echo "locked" > "$STATE_FILE"
elif [ "$1" = "unlock" ]; then
    echo "unlocked" > "$STATE_FILE"
fi
