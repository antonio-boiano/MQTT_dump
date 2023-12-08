#!/bin/bash

# Find the process ID (PID) of the running acquisition script
acq_pid=$(pgrep -f "python3 mqtt_acquire.py")

# Check if the acquisition script process is running
if [ -n "$acq_pid" ]; then
    # Terminate the acquisition script
    kill "$acq_pid"
    echo "Acquisition script terminated."
else
    echo "Acquisition script is not running."
fi

# Find the process ID (PID) of the running acquisition script
acq_pid=$(pgrep -f "python3 mqtt_compress.py")

# Check if the acquisition script process is running
if [ -n "$acq_pid" ]; then
    # Terminate the acquisition script
    kill "$acq_pid"
    echo "Compression script terminated."
else
    echo "Compression script is not running."
fi
