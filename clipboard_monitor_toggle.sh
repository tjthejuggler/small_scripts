#!/bin/bash

# Read the current status from the status file
if [ -f ~/clipboard_monitoring_status.txt ]; then
    status=$(cat ~/clipboard_monitoring_status.txt)
else
    status="off"
fi

# Toggle the status
if [ "$status" == "off" ]; then
    echo "on" > ~/clipboard_monitoring_status.txt
    notify-send "Clipboard monitoring is on."
else
    echo "off" > ~/clipboard_monitoring_status.txt
    notify-send "Clipboard monitoring is off."
fi
