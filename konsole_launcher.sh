#!/bin/bash

# File to store current window index
INDEX_FILE="/tmp/konsole_window_index"

# Function to check if Konsole is running
is_konsole_running() {
    pgrep -x konsole > /dev/null
}

# Function to get all Konsole windows
get_konsole_windows() {
    # Debug: List all windows with their classes
    echo "Listing all windows and their classes:" >&2
    xdotool search --class "." getwindowclassname %@ | grep -i "konsole" >&2
    
    # Get Konsole windows
    windows=$(xdotool search --class "konsole" 2>/dev/null || xdotool search --class "org.kde.konsole" 2>/dev/null)
    echo "Found Konsole windows: $windows" >&2
    echo "$windows"
}

# Function to focus Konsole window
focus_konsole() {
    local windows=($(get_konsole_windows))
    local num_windows=${#windows[@]}
    
    echo "Number of Konsole windows found: $num_windows" >&2
    
    if [ $num_windows -eq 0 ]; then
        echo "No Konsole windows found" >&2
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
    
    # Focus the window using multiple methods
    local window_id="${windows[$next_index]}"
    echo "Attempting to focus window ID: $window_id" >&2
    
    # Try multiple focus methods
    xdotool windowactivate "$window_id"
    xdotool windowfocus "$window_id"
    xdotool windowraise "$window_id"
    wmctrl -ia "$window_id"
    
    # If we were at -1, this is first focus
    if [ $current_index -eq -1 ]; then
        notify-send "Konsole" "Brought to front"
    else
        notify-send "Konsole" "Cycling to window $((next_index + 1)) of $num_windows"
    fi
    
    return 0
}

echo "Checking if Konsole is running..."
if is_konsole_running; then
    echo "Konsole is running. Attempting to bring to front..."
    if ! focus_konsole; then
        notify-send "Konsole" "Running, but couldn't bring to front"
    fi
else
    echo "Konsole is not running. Attempting to start..."
    # Reset index file when starting Konsole
    echo "-1" > "$INDEX_FILE"
    
    if command -v konsole &> /dev/null; then
        # Force X11 mode and disable Wayland for Qt
        export QT_QPA_PLATFORM=xcb
        export DISABLE_QT_WAYLAND=1
        konsole &
        notify-send "Konsole" "Starting..."
        echo "Waiting for Konsole to start..."
        for i in {1..10}; do
            sleep 1
            if is_konsole_running; then
                echo "Konsole started successfully."
                notify-send "Konsole" "Started successfully"
                focus_konsole
                exit 0
            fi
        done
        echo "Failed to detect Konsole running after 10 seconds."
        notify-send "Konsole" "Failed to start within 10 seconds"
    else
        echo "Error: Konsole command not found"
        notify-send "Konsole" "Error: Konsole command not found"
    fi
fi

echo "Script execution completed."
