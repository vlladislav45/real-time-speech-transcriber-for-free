#!/bin/bash

# Run Fast Speech Transcriber
# This script runs the fast version of the speech transcriber

echo "Starting Fast Speech Transcriber..."

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Make sure dependencies are installed."
fi

# Run the fast transcriber
python transcriber_fast.py 