#!/usr/bin/env bash
# =============================================================================
# HotelEyes - Toggle Script
# Run from anywhere: bash /opt/hoteleyes/hoteleyes.sh
# No sudo password needed (sudoers rule installed by setup.sh)
# Toggles motion ON/OFF and manages sleep inhibitor & alarm services
# =============================================================================

INHIBIT_PID_FILE="/tmp/hoteleyes-inhibit.pid"
ALARM_SERVER_PID_FILE="/tmp/hoteleyes-alarm-server.pid"
ALARM_SOUND_PID_FILE="/tmp/hoteleyes-alarm-sound.pid"
ALARM_STATE_FILE="/tmp/hoteleyes-alarm-state.json"

stop_inhibitor() {
    if [[ -f "$INHIBIT_PID_FILE" ]]; then
        kill "$(cat "$INHIBIT_PID_FILE")" 2>/dev/null || true
        rm -f "$INHIBIT_PID_FILE"
    fi
}

start_inhibitor() {
    stop_inhibitor
    sudo systemd-inhibit --what=sleep:idle --who="HotelEyes" \
        --why="Security camera monitoring active" --mode=block \
        sleep infinity &
    echo $! > "$INHIBIT_PID_FILE"
}

stop_alarm_services() {
    if [[ -f "$ALARM_SERVER_PID_FILE" ]]; then
        kill "$(cat "$ALARM_SERVER_PID_FILE")" 2>/dev/null || true
        rm -f "$ALARM_SERVER_PID_FILE"
    fi
    if [[ -f "$ALARM_SOUND_PID_FILE" ]]; then
        kill "$(cat "$ALARM_SOUND_PID_FILE")" 2>/dev/null || true
        rm -f "$ALARM_SOUND_PID_FILE"
    fi
}

start_alarm_services() {
    stop_alarm_services
    
    # Initialize alarm state to disabled by default
    echo '{"enabled": false, "triggered": false}' > "$ALARM_STATE_FILE"
    chmod 666 "$ALARM_STATE_FILE" 2>/dev/null || true

    # Start the web server
    python3 /opt/hoteleyes/alarm_web_server.py &>/dev/null &
    echo $! > "$ALARM_SERVER_PID_FILE"

    # Start the alarm sound loop
    /opt/hoteleyes/alarm_sound.sh &>/dev/null &
    echo $! > "$ALARM_SOUND_PID_FILE"
}

if systemctl is-active --quiet motion; then
    # Currently ON -> turn OFF
    sudo systemctl stop motion
    stop_inhibitor
    stop_alarm_services
    echo "HotelEyes OFF - monitoring stopped"
else
    # Currently OFF -> turn ON
    start_inhibitor
    start_alarm_services
    sudo systemctl start motion
    echo "HotelEyes ON - monitoring started"
    IP=$(tailscale ip -4 2>/dev/null || echo '100.79.198.62')
    echo "  Live stream & Alarm control: http://${IP}:8082/"
fi
