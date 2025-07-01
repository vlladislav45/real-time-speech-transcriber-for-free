#!/bin/bash

# View Transcription Logs
# This script runs the log viewer application

echo "Starting Log Viewer..."

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Make sure dependencies are installed."
fi

# Run the log viewer
python log_viewer.py 