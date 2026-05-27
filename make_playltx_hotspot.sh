#!/bin/bash

SSID="PLAYLTX"
PASS="pixelprops256"

# 1. Clean up
nmcli con delete "$SSID" > /dev/null 2>&1

# 2. Create with Watch-Friendly settings:
# - band bg: Forces 2.4GHz (Watches often can't see 5GHz)
# - proto rsn: Forces WPA2 (Watches hate WPA3)
# - key-mgmt wpa-psk: Standard WPA2 security
nmcli con add type wifi ifname "*" con-name "$SSID" autoconnect yes ssid "$SSID" \
    802-11-wireless.mode ap \
    802-11-wireless.band bg \
    802-11-wireless-security.key-mgmt wpa-psk \
    802-11-wireless-security.proto rsn \
    802-11-wireless-security.group ccmp \
    802-11-wireless-security.pairwise ccmp \
    802-11-wireless-security.psk "$PASS" \
    ipv4.method shared

# 3. Bring it up
nmcli con up "$SSID"