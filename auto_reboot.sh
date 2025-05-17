#!/bin/bash

SERVER_PATH="./main.py"

# Adds a delay before rebooting the server
DELAY=0  # number of seconds to wait


_END_LOOP=false


cleanup() {
    echo -e "\nKeyboard interrupt detected; waiting for server to shutdown..."
    _END_LOOP=true
}

# bind Ctrl+C to the cleanup() function
trap cleanup SIGINT

while true
do
    python3 "$SERVER_PATH"

    if $_END_LOOP; then
        exit 0
    fi

    echo
    echo -e "\nthe server has crashed."
    for ((count=DELAY; count>0; count--))
    do
        echo "rebooting in $count second."
        sleep 1
    done
done