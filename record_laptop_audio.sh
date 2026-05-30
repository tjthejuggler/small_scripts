#!/bin/bash

# Laptop Audio Recording Script
# Records system audio output even when the physical volume is turned down or muted.
# Uses a virtual null sink and loopback to route audio safely.
# Created: 2026-05-29

set -e

# Default values
DURATION_STR="6.5h"
OUTPUT_FILE=""

# Function to display usage
usage() {
    echo "Usage: $0 [duration] [output_file]"
    echo "  duration:    Duration to record (e.g., 6.5h, 30m, 120s, or raw seconds). Default: 6.5h"
    echo "  output_file: Path to save the recording (e.g., recording.mp3). Default: recording_YYYYMMDD_HHMMSS.mp3"
    echo ""
    echo "Examples:"
    echo "  $0 6.5h"
    echo "  $0 10m test.mp3"
    exit 1
}

# Parse arguments
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
fi

if [ -n "$1" ]; then
    DURATION_STR="$1"
fi

if [ -n "$2" ]; then
    OUTPUT_FILE="$2"
fi

# Parse duration string to seconds
parse_duration() {
    local input="$1"
    if [[ "$input" =~ ^([0-9]+(\.[0-9]+)?)[hH]$ ]]; then
        # Hours
        echo "$(echo "${BASH_REMATCH[1]} * 3600" | bc -l | cut -d. -f1)"
    elif [[ "$input" =~ ^([0-9]+(\.[0-9]+)?)[mM]$ ]]; then
        # Minutes
        echo "$(echo "${BASH_REMATCH[1]} * 60" | bc -l | cut -d. -f1)"
    elif [[ "$input" =~ ^([0-9]+)[sS]?$ ]]; then
        # Seconds
        echo "${BASH_REMATCH[1]}"
    else
        echo "Error: Invalid duration format '$input'. Use e.g. 6.5h, 30m, 120s" >&2
        exit 1
    fi
}

# Check dependencies
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is required but not installed." >&2
    exit 1
fi

if ! command -v pactl &> /dev/null; then
    echo "Error: pactl (PulseAudio/PipeWire control) is required but not installed." >&2
    exit 1
fi

if ! command -v bc &> /dev/null; then
    echo "Error: bc (calculator) is required but not installed." >&2
    exit 1
fi

DURATION_SECS=$(parse_duration "$DURATION_STR")

# Set default output file if not provided
if [ -z "$OUTPUT_FILE" ]; then
    OUTPUT_FILE="recording_$(date +%Y%m%d_%H%M%S).mp3"
fi

# Get original default sink
ORIGINAL_SINK=$(pactl get-default-sink)
if [ -z "$ORIGINAL_SINK" ]; then
    echo "Error: Could not detect default audio sink." >&2
    exit 1
fi

# Variables to track loaded modules for cleanup
NULL_SINK_ID=""
LOOPBACK_ID=""
CLEANED_UP=0

# Function to move all active audio streams to a target sink
move_all_inputs() {
    local target_sink="$1"
    pactl list short sink-inputs | while read -r id _; do
        if [ -n "$id" ]; then
            pactl move-sink-input "$id" "$target_sink" 2>/dev/null || true
        fi
    done
}

# Cleanup function to restore original audio state
cleanup() {
    if [ "$CLEANED_UP" -eq 1 ]; then
        return
    fi
    CLEANED_UP=1
    
    echo ""
    echo "Restoring original audio configuration..."
    
    # Move active streams back to original sink
    if [ -n "$ORIGINAL_SINK" ]; then
        move_all_inputs "$ORIGINAL_SINK"
        pactl set-default-sink "$ORIGINAL_SINK" || true
    fi
    
    # Unload loopback module
    if [ -n "$LOOPBACK_ID" ]; then
        echo "Unloading loopback module..."
        pactl unload-module "$LOOPBACK_ID" || true
    fi
    
    # Unload null sink module
    if [ -n "$NULL_SINK_ID" ]; then
        echo "Unloading virtual null sink..."
        pactl unload-module "$NULL_SINK_ID" || true
    fi
    
    echo "Cleanup complete."
}

# Register cleanup trap for exit, interrupt, and termination signals
trap cleanup EXIT INT TERM

echo "=================================================="
echo "Laptop Audio Recording Script"
echo "=================================================="
echo "Original Default Sink: $ORIGINAL_SINK"
echo "Recording Duration:    $DURATION_SECS seconds ($DURATION_STR)"
echo "Output File:           $OUTPUT_FILE"
echo "--------------------------------------------------"
echo "Setting up virtual audio routing..."

# 1. Create virtual null sink
NULL_SINK_ID=$(pactl load-module module-null-sink sink_name=record_null_sink sink_properties=device.description="Record_Null_Sink")
if [ -z "$NULL_SINK_ID" ]; then
    echo "Error: Failed to load virtual null sink module." >&2
    exit 1
fi

# 2. Set virtual null sink as default
pactl set-default-sink record_null_sink

# 3. Move all currently playing streams to the virtual sink
move_all_inputs record_null_sink

# 4. Create loopback from virtual sink monitor to original physical sink
# This allows the user to still hear audio if physical volume is up,
# but turning physical volume down/muting won't affect the virtual sink recording.
LOOPBACK_ID=$(pactl load-module module-loopback source=record_null_sink.monitor sink="$ORIGINAL_SINK")
if [ -z "$LOOPBACK_ID" ]; then
    echo "Error: Failed to load loopback module." >&2
    exit 1
fi

echo "Virtual audio routing configured successfully."
echo "--------------------------------------------------"
echo "Note: You can safely turn down or mute your laptop volume."
echo "The recording will still capture the audio at full volume."
echo "Press Ctrl+C to stop recording early and save."
echo "================================================--"
echo "Recording started..."

# Run ffmpeg to record from the virtual sink's monitor
# -y: Overwrite output files without asking
# -f pulse: Use PulseAudio input device
# -i record_null_sink.monitor: Record from the monitor of our virtual sink
# -t: Limit recording duration
# -acodec libmp3lame: Encode to MP3
# -ab 192k: 192 kbps bitrate (high quality stereo)
ffmpeg -y -f pulse -i record_null_sink.monitor -t "$DURATION_SECS" -acodec libmp3lame -ab 192k "$OUTPUT_FILE"

echo "Recording finished successfully."
