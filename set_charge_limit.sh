#!/bin/bash
# Set your desired charge limit (0-100) below
sleep 10
CHARGE_LIMIT=75
echo $CHARGE_LIMIT | sudo tee /sys/class/power_supply/BAT0/charge_control_end_threshold
