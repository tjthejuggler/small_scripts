#!/usr/bin/env bash
# Helper script to install HotelEyes updates
# Run this script with sudo: sudo bash install_hoteleyes.sh

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (with sudo)" 
   exit 1
fi

echo "Copying files to /opt/hoteleyes/..."
cp ./alarm.wav /opt/hoteleyes/alarm.wav
cp ./alarm_sound.sh /opt/hoteleyes/alarm_sound.sh
cp ./capture_additional.sh /opt/hoteleyes/capture_additional.sh
cp ./alarm_web_server.py /opt/hoteleyes/alarm_web_server.py
cp ./on_picture_save.sh /opt/hoteleyes/on_picture_save.sh
cp ./hoteleyes.sh /opt/hoteleyes/hoteleyes.sh

echo "Setting permissions..."
chmod +x /opt/hoteleyes/*.sh

echo "HotelEyes files installed successfully!"
