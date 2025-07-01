#!/bin/bash

# Run Improved Speech Transcriber
# This script runs the improved version of the speech transcriber

echo "Starting Improved Speech Transcriber..."

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Make sure dependencies are installed."
fi

# Run the improved transcriber
python transcriber_improved.py 