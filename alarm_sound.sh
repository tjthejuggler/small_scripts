#!/usr/bin/env bash
# HotelEyes - Alarm Sound Loop Script
# Plays alarm sound if alarm is enabled and triggered

ALARM_STATE_FILE="/tmp/hoteleyes-alarm-state.json"
ALARM_WAV="/opt/hoteleyes/alarm.wav"

# Ensure state file exists
if [[ ! -f "$ALARM_STATE_FILE" ]]; then
    echo '{"enabled": false, "triggered": false}' > "$ALARM_STATE_FILE"
    chmod 666 "$ALARM_STATE_FILE"
fi

while true; do
    # Read state using python to parse json safely
    ENABLED=$(python3 -c "import json; print(json.load(open('$ALARM_STATE_FILE')).get('enabled', False))" 2>/dev/null || echo "False")
    TRIGGERED=$(python3 -c "import json; print(json.load(open('$ALARM_STATE_FILE')).get('triggered', False))" 2>/dev/null || echo "False")

    if [[ "$ENABLED" == "True" && "$TRIGGERED" == "True" ]]; then
        if command -v paplay &>/dev/null; then
            paplay "$ALARM_WAV" 2>/dev/null || aplay "$ALARM_WAV" 2>/dev/null || ffplay -nodisp -autoexit "$ALARM_WAV" &>/dev/null
        elif command -v aplay &>/dev/null; then
            aplay "$ALARM_WAV" 2>/dev/null || ffplay -nodisp -autoexit "$ALARM_WAV" &>/dev/null
        else
            ffplay -nodisp -autoexit "$ALARM_WAV" &>/dev/null
        fi
        sleep 1
    else
        sleep 1
    fi
done
