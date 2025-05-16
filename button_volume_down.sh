#!/bin/bash

# Script for volume down mouse button
# This script calls the mode manager with the button name
# The mode manager will track when this button was pressed

# Debugging notification (commented out)
# notify-send "Button Script" "Volume Down Button Pressed" -t 2000

# Call the mode manager
/home/twain/Projects/small_scripts/mouse_modes/mode_manager.sh volume_down