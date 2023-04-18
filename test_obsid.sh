#!/bin/bash

echo "Starting script..."

if wmctrl -x -l | grep -q 'obsidian'; then
  echo "Obsidian window found, bringing to front..."
  wmctrl -xa 'obsidian'
else
  echo "Obsidian window not found, starting new instance..."
  /home/lunkwill/programs/obsidian/Obsidian-1.1.16.AppImage &
fi

echo "Script complete."
