#!/bin/bash

if [[ -n "$(xsel -o)" ]]; then
    xdotool key ctrl+c && sleep 0.1 && if wmctrl -xl | grep -q 'firefox'; then wmctrl -xa 'firefox'; else /snap/bin/firefox & fi && sleep 0.1 && xdotool key ctrl+t && xdotool key ctrl+l && xdotool key ctrl+v && xdotool key Return
fi
