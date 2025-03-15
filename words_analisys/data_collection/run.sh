#!/bin/bash

# Directory containing chunk files
CHUNK_DIR="output_chunks"
# Number of parallel processes to run
MAX_PROCESSES=12

# Trap SIGINT to terminate all child processes when Ctrl+C is pressed
trap 'echo "Stopping all processes..."; kill 0' SIGINT

# Function to run extract.py on a single file, with logging
process_file() {
    local chunk_file="$1"
    local log_file="logs/$(basename "$chunk_file" .xlsx)_log.txt"

    # Create logs directory if it doesn't exist
    mkdir -p logs

    # Log process start with PID
    echo "Starting processing of $chunk_file with PID $$" | tee -a "$log_file"

    # Use unbuffer to stream output to log file in real-time
    unbuffer python3 extract.py "$chunk_file" --column_name "Abstract" | tee -a "$log_file"

    # Log process end
    echo "Completed processing of $chunk_file with PID $$" | tee -a "$log_file"
}

# Export the function so it's available to parallel execution
export -f process_file

# Use find to list each chunk file, then run them in parallel
find "$CHUNK_DIR" -name "*.xlsx" | \
    xargs -P "$MAX_PROCESSES" -I {} bash -c 'process_file "$@"' _ {}
