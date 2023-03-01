#!/bin/bash



# Initialize variable to store the current clipboard contents
current_contents=""

while true; do
    # Check the current clipboard contents
    new_contents="$(xclip -selection clipboard -o)"
    # If the clipboard contents have changed, append the new contents to the file
    if [ "$new_contents" != "$current_contents" ]; then
        # Read the current status from the status file
        if [ -f ~/clipboard_monitoring_status.txt ]; then
            status=$(cat ~/clipboard_monitoring_status.txt)
        else
            status="off"
        fi

        # If the status is off, exit the script
        if [ "$status" != "off" ]; then
            echo "$new_contents" >> ~/clipboard.txt
            current_contents="$new_contents"
        fi

    fi
    # Sleep for a short period of time before checking again
    sleep 0.5
done
