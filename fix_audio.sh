#!/bin/bash

# Script to fix audio issues by restarting audio services and launching pavucontrol
# Created: $(date)

echo "Starting audio fix script..."

# Restart audio services
echo "Restarting wireplumber..."
systemctl --user restart wireplumber
sleep 2

echo "Restarting pipewire.service..."
systemctl --user restart pipewire.service
sleep 2

echo "Restarting pipewire-pulse.service..."
systemctl --user restart pipewire-pulse.service
sleep 3

# Launch pavucontrol in the background
echo "Launching pavucontrol..."
pavucontrol &

echo "Audio fix script completed."