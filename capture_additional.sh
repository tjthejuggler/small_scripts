#!/usr/bin/env bash
# HotelEyes - Capture 5 additional frames at 0.5s, 1.5s, 2.5s, 3.5s, 4.5s
# Sends them as a single Telegram media group (one message/text block)

BOT_TOKEN="8646934924:AAF_BlIqpWhbq0tPi2Ryw34RIleKooYKmwo"
CHAT_ID="1888591489"
LIVE_URL="$1"

STREAM_URL="http://localhost:8081/"
TMP_DIR="/tmp/hoteleyes_captures"
mkdir -p "$TMP_DIR"

capture_frame() {
    local delay="$1"
    local num="$2"
    sleep "$delay"
    
    local out_file="${TMP_DIR}/snap_${num}_$(date +%s).jpg"
    # Capture 1 frame from the motion stream
    ffmpeg -y -i "$STREAM_URL" -vframes 1 -f image2 "$out_file" &>/dev/null
    
    if [[ -f "$out_file" ]]; then
        echo "$out_file"
    fi
}

# Run the captures in background so we don't block the main script
(
    # Delays relative to start of this script:
    # 1st: 0.5s
    # 2nd: 1.5s (0.5 + 1.0)
    # 3rd: 2.5s (1.5 + 1.0)
    # 4th: 3.5s (2.5 + 1.0)
    # 5th: 4.5s (3.5 + 1.0)
    
    PIC1=$(capture_frame 0.5 1)
    PIC2=$(capture_frame 1.0 2)
    PIC3=$(capture_frame 1.0 3)
    PIC4=$(capture_frame 1.0 4)
    PIC5=$(capture_frame 1.0 5)
    
    # Build the media group JSON array and curl file arguments
    # Telegram sendMediaGroup API takes an array of InputMediaPhoto objects
    # and multipart form files matching the media attachment names.
    
    MEDIA_JSON="["
    CURL_ARGS=()
    COUNT=0
    
    for pic in "$PIC1" "$PIC2" "$PIC3" "$PIC4" "$PIC5"; do
        if [[ -n "$pic" && -f "$pic" ]]; then
            if [[ $COUNT -gt 0 ]]; then
                MEDIA_JSON="${MEDIA_JSON},"
            fi
            
            # The first photo in the group gets the caption/text
            if [[ $COUNT -eq 0 ]]; then
                MEDIA_JSON="${MEDIA_JSON}{\"type\":\"photo\",\"media\":\"attach://file_${COUNT}\",\"caption\":\"Additional movement frames captured over the next 5 seconds. Live stream: ${LIVE_URL}\"}"
            else
                MEDIA_JSON="${MEDIA_JSON}{\"type\":\"photo\",\"media\":\"attach://file_${COUNT}\"}"
            fi
            
            CURL_ARGS+=("-F" "file_${COUNT}=@${pic}")
            COUNT=$((COUNT + 1))
        fi
    done
    MEDIA_JSON="${MEDIA_JSON}]"
    
    if [[ $COUNT -gt 0 ]]; then
        # Send all 5 photos in a single media group message!
        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMediaGroup" \
            -F "chat_id=${CHAT_ID}" \
            -F "media=${MEDIA_JSON}" \
            "${CURL_ARGS[@]}" >/dev/null
            
        # Clean up files
        for pic in "$PIC1" "$PIC2" "$PIC3" "$PIC4" "$PIC5"; do
            rm -f "$pic" 2>/dev/null
        done
    fi
) &
