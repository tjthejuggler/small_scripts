#!/bin/bash

# Get the default sink number
sink=$(pactl get-default-sink)

# Increase volume by 10%
pactl set-sink-volume @DEFAULT_SINK@ +10%

# Get current volume
volume=$(pactl list sinks | grep -A 15 "$sink" | grep "Volume:" | head -n 1 | awk '{print $5}')

# Show notification
notify-send "Volume Up" "Current Volume: $volume" -t 1500
