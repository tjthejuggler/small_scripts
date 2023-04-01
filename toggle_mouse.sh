#!/bin/bash

config_file="$HOME/.config/mouse_toggler"

#wait 1 second
sleep .2

if [ ! -f "$config_file" ]; then
    echo "right" > "$config_file"
fi

current_mode=$(cat "$config_file")

if [ "$current_mode" = "right" ]; then
    new_mode="middle"
else
    new_mode="right"
fi

echo "$new_mode" > "$config_file"

# Dynamically detect the device ID of the "Surface Arc Mouse"
device_id=$(xinput list | grep -E 'Surface Arc Mouse\s+id=[0-9]+\s+\[slave\s+pointer' | grep -oP 'id=\K\d+')

case "$new_mode" in
    middle)
        xinput set-button-map "$device_id" 1 3 2 4 5 6 7 8 9
        notify-send "Mouse button toggled (Device ID: $device_id)" "Right mouse button now acts as middle button."
        ;;
    right)
        xinput set-button-map "$device_id" 1 2 3 4 5 6 7 8 9
        notify-send "Mouse button toggled (Device ID: $device_id)" "Right mouse button now acts as right button."
        ;;
esac

# Update the system tray icon
pkill -USR1 -f "python3 toggle_mouse_icon.py"
