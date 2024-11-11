#!/bin/bash

# File to store current window index
INDEX_FILE="/tmp/firefox_window_index"

# Function to check if Firefox is running
is_firefox_running() {
    pgrep -f 'firefox132' > /dev/null
}

# Function to get all Firefox windows
get_firefox_windows() {
    wmctrl -l | grep -i "mozilla firefox" | cut -d' ' -f1
}

# Function to focus Firefox window
focus_firefox() {
    local windows=($(get_firefox_windows))
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
        notify-send "Firefox" "Brought to front"
    else
        notify-send "Firefox" "Cycling to window $((next_index + 1)) of $num_windows"
    fi
    
    return 0
}

echo "Checking if Firefox is running..."
if is_firefox_running; then
    echo "Firefox is running. Attempting to bring to front..."
    if ! focus_firefox; then
        notify-send "Firefox" "Running, but couldn't bring to front"
    fi
else
    echo "Firefox is not running. Attempting to start..."
    # Reset index file when starting Firefox
    echo "-1" > "$INDEX_FILE"
    
    if command -v firefox132 &> /dev/null; then
        # Force X11 mode and start Firefox
        export MOZ_ENABLE_WAYLAND=0
        firefox132 &
        notify-send "Firefox" "Starting..."
        echo "Waiting for Firefox to start..."
        for i in {1..10}; do
            sleep 1
            if is_firefox_running; then
                echo "Firefox started successfully."
                notify-send "Firefox" "Started successfully"
                focus_firefox
                exit 0
            fi
        done
        echo "Failed to detect Firefox running after 10 seconds."
        notify-send "Firefox" "Failed to start within 10 seconds"
    else
        echo "Error: Firefox command not found"
        notify-send "Firefox" "Error: Firefox command not found"
    fi
fi

echo "Script execution completed."
