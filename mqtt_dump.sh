#!/bin/bash

# Parse input arguments
max_size=$1 #IN MB
delay=$1 # IN sec
parent_output_folder=$2

# Validate the parent output folder
if [ ! -d "$parent_output_folder" ]; then
    echo "Parent output folder '$parent_output_folder' does not exist."
    exit 1
fi

# Get the current timestamp
timestamp=$(date '+%Y%m%d_%H%M%S')

# Create a folder based on the timestamp inside the provided parent folder
output_folder="${parent_output_folder}/${timestamp}"
mkdir -p "$output_folder"

# Execute the acquisition script in the background
nohup python3 mqtt_acquire.py --maxsize "$max_size" --savedir "$output_folder" & disown

# Give some time before starting the compression script (adjust as needed)
sleep 5

# Execute the compression script in the background
nohup python3 mqtt_compress.py "$output_folder" --maxsize "$max_size" --delay "$delay" & disown

