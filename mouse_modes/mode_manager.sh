#!/bin/bash

# Configuration
MODE_FILE="/tmp/mouse_mode_current"
LAST_VOLUME_PRESS_FILE="/tmp/mouse_mode_last_volume_press"
MODE_TIMEOUT=1 # seconds

# Available modes
MODES=("default" "custom_mode")
NUM_MODES=${#MODES[@]}

# Initialize mode file if it doesn't exist
if [ ! -f "$MODE_FILE" ]; then
    echo "0" > "$MODE_FILE" # Start with default mode (index 0)
fi

# Function to get current mode index
get_current_mode_index() {
    if [ -f "$MODE_FILE" ]; then
        cat "$MODE_FILE"
    else
        echo "0" # Default to first mode if file doesn't exist
    fi
}

# Function to get current mode name
get_current_mode_name() {
    local index=$(get_current_mode_index)
    echo "${MODES[$index]}"
}

# Function to update last volume press time
update_volume_press_time() {
    date +%s > "$LAST_VOLUME_PRESS_FILE"
}

# Function to check if volume button was pressed recently
was_volume_pressed_recently() {
    if [ ! -f "$LAST_VOLUME_PRESS_FILE" ]; then
        return 1 # False if file doesn't exist
    fi
    
    local last_press=$(cat "$LAST_VOLUME_PRESS_FILE")
    local current_time=$(date +%s)
    local time_diff=$((current_time - last_press))
    
    if [ $time_diff -le $MODE_TIMEOUT ]; then
        return 0 # True if pressed within timeout
    else
        return 1 # False if not pressed recently
    fi
}

# Function to switch to next mode
switch_to_next_mode() {
    local current_index=$(get_current_mode_index)
    local next_index=$(( (current_index + 1) % NUM_MODES ))
    
    echo "$next_index" > "$MODE_FILE"
    
    local next_mode="${MODES[$next_index]}"
    notify-send "Mouse Mode Switched" "Now using: $next_mode mode" -t 2000
}

# Function to handle volume up press with mode switching logic
handle_volume_up() {
    if was_volume_pressed_recently; then
        # Volume was pressed recently, just update the time and increase volume
        update_volume_press_time
        # Execute the actual volume up script
        /home/twain/Projects/small_scripts/volume_up_10.sh
    else
        # Volume wasn't pressed recently, switch mode and update time
        # But don't increase volume when switching modes
        update_volume_press_time
        switch_to_next_mode
    fi
}

# Function to handle volume down press (just updates time)
handle_volume_down() {
    update_volume_press_time
    # Execute the actual volume down script
    /home/twain/Projects/small_scripts/volume_down_10.sh
}

# Function to execute script based on current mode
execute_script() {
    local button_name="$1"
    local mode_name=$(get_current_mode_name)
    
    # Debug notification (commented out)
    # notify-send "Mode Manager" "Button: $button_name, Mode: $mode_name" -t 2000
    
    local script_path="/home/twain/Projects/small_scripts/mouse_modes/$mode_name/$button_name.sh"
    
    # Check if mode-specific script exists
    if [ -x "$script_path" ]; then
        # Debug notification (commented out)
        # notify-send "Mode Manager" "Executing: $script_path" -t 2000
        
        # Execute mode-specific script
        "$script_path"
    else
        # Fall back to default script if mode-specific doesn't exist
        local default_script="/home/twain/Projects/small_scripts/mouse_modes/default/$button_name.sh"
        if [ -x "$default_script" ]; then
            # Debug notification (commented out)
            # notify-send "Mode Manager" "Executing default: $default_script" -t 2000
            
            "$default_script"
        else
            notify-send "Mouse Button Error" "No script found for $button_name in $mode_name mode" -t 2000
        fi
    fi
}

# Main execution based on first argument
case "$1" in
    "volume_up")
        # Debug notification (commented out)
        # notify-send "Mode Manager" "Volume Up Button Pressed" -t 2000
        handle_volume_up
        ;;
    "volume_down")
        # Debug notification (commented out)
        # notify-send "Mode Manager" "Volume Down Button Pressed" -t 2000
        handle_volume_down
        ;;
    *)
        # For all other buttons, execute the appropriate script based on mode
        execute_script "$1"
        ;;
esac

# Debug notification at the end (commented out)
# notify-send "Mode Manager" "Script execution completed" -t 2000