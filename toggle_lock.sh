#!/bin/bash
STATE_FILE="$HOME/.pc_lock_state"

# Read the file to see what the native system told us the state is
if [ -f "$STATE_FILE" ] && [ "$(cat "$STATE_FILE")" = "locked" ]; then
    loginctl unlock-session
else
    loginctl lock-session
fi
