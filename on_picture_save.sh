#!/usr/bin/env bash
# HotelEyes - Telegram Snapshot Notification & Alarm Trigger
# Called by motion on_picture_save event
# Arg $1 = full path to saved image file

PHOTO_FILE="$1"
BOT_TOKEN="8646934924:AAF_BlIqpWhbq0tPi2Ryw34RIleKooYKmwo"
CHAT_ID="1888591489"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
ALARM_STATE_FILE="/tmp/hoteleyes-alarm-state.json"

[[ ! -f "$PHOTO_FILE" ]] && exit 0

# Get Tailscale IP or fallback
IP=$(tailscale ip -4 2>/dev/null || echo "100.79.198.62")
LIVE_URL="http://${IP}:8082/"

# 1. Send the initial photo immediately with the live stream URL
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto" \
    -F "chat_id=${CHAT_ID}" \
    -F "photo=@${PHOTO_FILE}" \
    -F "caption=Motion detected at ${TIMESTAMP}. Live stream: ${LIVE_URL}" \
    > /dev/null 2>&1 &

# 2. Trigger the alarm state if enabled
if [[ -f "$ALARM_STATE_FILE" ]]; then
    # Read enabled state
    ENABLED=$(python3 -c "import json; print(json.load(open('$ALARM_STATE_FILE')).get('enabled', False))" 2>/dev/null || echo "False")
    if [[ "$ENABLED" == "True" ]]; then
        # Set triggered to true
        python3 -c "import json; f=open('$ALARM_STATE_FILE','r+'); d=json.load(f); d['triggered']=True; f.seek(0); json.dump(d,f); f.truncate()" 2>/dev/null
    fi
fi

# 3. Launch the additional 5 frames capture script in the background
/opt/hoteleyes/capture_additional.sh "$LIVE_URL" >/dev/null 2>&1 &

exit 0
