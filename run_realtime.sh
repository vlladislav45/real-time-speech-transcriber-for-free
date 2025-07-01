#!/bin/bash

# Run Real-time Speech Transcriber
# This script runs the real-time version of the speech transcriber

echo "Starting Real-time Speech Transcriber..."

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Make sure dependencies are installed."
fi

# Run the real-time transcriber
python transcriber_realtime.py 