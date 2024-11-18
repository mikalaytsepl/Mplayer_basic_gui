#!/bin/bash

start_mplayer() {
    local path="$1"

    # Expand the path if ~ is used
    path=$(eval echo "$path")

    if [[ -f $path ]]; then
        # Start the controls program
        ./controls &
        CONTROLS_PID=$!

        # Wait for controls to be fully initialized
        while ! ps -p $CONTROLS_PID > /dev/null; do
            echo "Waiting for controls to start..."
            sleep 1
        done

        echo "Controls program is running."

        # Start the Python UI
        ./.venv/bin/python3.11 userinterface.py &

        sleep 2  # Allow the UI to initialize

        echo "Starting MPlayer with file: $path"

        # Start MPlayer
        mplayer -nolirc -input file="/tmp/fifo_for_mplayer" -slave -quiet "$path"
    else
        echo "Video you are trying to play was not found."
    fi
}

start_mplayer "$@"
