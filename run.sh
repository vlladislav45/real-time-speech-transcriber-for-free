#!/bin/bash

# Speech Transcriber Runner Script
# This script helps you choose and run different versions of the speech transcriber

echo "=== Speech Transcriber ==="
echo ""
echo "Choose a version to run:"
echo "1. Standard Version (transcriber.py)"
echo "2. Improved Version (transcriber_improved.py)"
echo "3. Fast Version (transcriber_fast.py)"
echo "4. Real-time Version (transcriber_realtime.py)"
echo "5. Log Viewer (log_viewer.py)"
echo "6. Exit"
echo ""

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Make sure dependencies are installed."
fi

# Function to run the selected version
run_version() {
    case $1 in
        1)
            echo "Starting Standard Version..."
            python transcriber.py
            ;;
        2)
            echo "Starting Improved Version..."
            python transcriber_improved.py
            ;;
        3)
            echo "Starting Fast Version..."
            python transcriber_fast.py
            ;;
        4)
            echo "Starting Real-time Version..."
            python transcriber_realtime.py
            ;;
        5)
            echo "Starting Log Viewer..."
            python log_viewer.py
            ;;
        6)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please choose 1-6."
            ;;
    esac
}

# Main loop
while true; do
    read -p "Enter your choice (1-6): " choice
    
    if [[ $choice =~ ^[1-6]$ ]]; then
        run_version $choice
        echo ""
        read -p "Press Enter to continue or Ctrl+C to exit..."
        echo ""
        echo "=== Speech Transcriber ==="
        echo ""
        echo "Choose a version to run:"
        echo "1. Standard Version (transcriber.py)"
        echo "2. Improved Version (transcriber_improved.py)"
        echo "3. Fast Version (transcriber_fast.py)"
        echo "4. Real-time Version (transcriber_realtime.py)"
        echo "5. Log Viewer (log_viewer.py)"
        echo "6. Exit"
        echo ""
    else
        echo "Invalid input. Please enter a number between 1 and 6."
    fi
done 