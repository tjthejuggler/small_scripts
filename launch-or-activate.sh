#!/bin/bash

if wmctrl -xl | grep -q "$1"; then
    wmctrl -xa "$1"
else
    "$1" &
fi
