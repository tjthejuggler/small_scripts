#!/bin/bash

# Path to Obsidian executable
OBSIDIAN_PATH="/home/twain/ProgramsUbuntu/obsidian-squashfs/obsidian"


# Function to check if Obsidian is running
is_obsidian_running() {
    pgrep -f "$OBSIDIAN_PATH" > /dev/null
}

# Function to focus Obsidian window
focus_obsidian() {
    if wmctrl -xa "obsidian.Obsidian"; then
        return 0
    elif wmctrl -xa "obsidian"; then
        return 0
    else
        obsidian_window=$(wmctrl -l | grep -i "obsidian" | head -n 1 | cut -d' ' -f1)
        if [ -n "$obsidian_window" ]; then
            wmctrl -ia "$obsidian_window"
            return 0
        fi
    fi
    return 1
}

if is_obsidian_running; then
    if focus_obsidian; then
        notify-send "Obsidian" "Brought to front"
    else
        notify-send "Obsidian" "Running, but couldn't bring to front"
    fi
else
    if [ -x "$OBSIDIAN_PATH" ]; then
        "$OBSIDIAN_PATH" --no-sandbox &
        notify-send "Obsidian" "Starting..."
        # Wait for Obsidian to start and then focus it
        for i in {1..10}; do
            sleep 1
            if is_obsidian_running; then
                focus_obsidian
                notify-send "Obsidian" "Started successfully"
                exit 0
            fi
        done
        notify-send "Obsidian" "Failed to start within 10 seconds"
    else
        notify-send "Obsidian" "Error: Obsidian executable not found"
    fi
fi
