#!/bin/bash
# Toggle VLC play/pause via MPRIS2 D-Bus interface.
# If VLC is not running, launch it.

VLC_BUS="org.mpris.MediaPlayer2.vlc"
MPRIS_PATH="/org/mpris/MediaPlayer2"
MPRIS_IFACE="org.mpris.MediaPlayer2.Player"

# Check if VLC is running
if dbus-send --session --dest="$VLC_BUS" --type=method_call \
    --print-reply "$MPRIS_PATH" org.freedesktop.DBus.Introspectable.Introspect \
    &>/dev/null; then
    # VLC is running — toggle play/pause
    dbus-send --session --dest="$VLC_BUS" --type=method_call \
        "$MPRIS_PATH" "${MPRIS_IFACE}.PlayPause"
else
    # VLC is not running — launch it
    nohup vlc &>/dev/null &
fi
