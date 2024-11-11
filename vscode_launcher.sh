#!/bin/bash

notify-send "VS Code Launcher" "Script starting..."

# File to store current window index
INDEX_FILE="/tmp/vscode_window_index"

# Function to check if VS Code is running
is_vscode_running() {
    pgrep -f '/usr/share/code/code' > /dev/null
}

# Function to get all VS Code windows
get_vscode_windows() {
    wmctrl -l | grep -iE "visual studio code|code.Code" | cut -d' ' -f1
}

# Function to focus VS Code window
focus_vscode() {
    local windows=($(get_vscode_windows))
    local num_windows=${#windows[@]}
    
    if [ $num_windows -eq 0 ]; then
        return 1
    fi
    
    # Get current index from file, default to -1
    local current_index=-1
    if [ -f "$INDEX_FILE" ]; then
        current_index=$(cat "$INDEX_FILE")
    fi
    
    # Calculate next index
    local next_index=$(( (current_index + 1) % num_windows ))
    
    # Store next index
    echo "$next_index" > "$INDEX_FILE"
    
    # Focus the window
    wmctrl -ia "${windows[$next_index]}"
    
    # If we were at -1, this is first focus
    if [ $current_index -eq -1 ]; then
        notify-send "VS Code" "Brought to front"
    else
        notify-send "VS Code" "Cycling to window $((next_index + 1)) of $num_windows"
    fi
    
    return 0
}

if is_vscode_running; then
    if ! focus_vscode; then
        notify-send "VS Code" "Running, but couldn't bring to front"
    fi
else
    # Reset index file when starting VS Code
    echo "-1" > "$INDEX_FILE"
    
    if command -v code &> /dev/null; then
        code &
        notify-send "VS Code" "Starting..."
        # Wait for VS Code to start and then focus it
        for i in {1..10}; do
            sleep 1
            if is_vscode_running; then
                focus_vscode
                notify-send "VS Code" "Started successfully"
                exit 0
            fi
        done
        notify-send "VS Code" "Failed to start within 10 seconds"
    else
        notify-send "VS Code" "Error: VS Code executable not found"
    fi
fi
