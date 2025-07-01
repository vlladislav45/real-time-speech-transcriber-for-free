#!/bin/bash

# Global Installation Script for Speech Transcriber
# This script installs the speech transcriber globally on macOS

echo "=== Speech Transcriber Global Installation ==="
echo "This script will install the speech transcriber globally on your system."
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Please install Homebrew first:"
    echo "https://brew.sh/"
    exit 1
fi

echo "Installing system dependencies..."
brew install portaudio python@3.11

echo ""
echo "Installing Python packages globally..."
pip3 install SpeechRecognition pyaudio

echo ""
echo "Installation complete!"
echo ""
echo "You can now run the speech transcriber using:"
echo "  python3 transcriber.py"
echo "  python3 transcriber_improved.py"
echo "  python3 transcriber_fast.py"
echo "  python3 transcriber_realtime.py"
echo "  python3 log_viewer.py"
echo ""
echo "Or use the shell scripts:"
echo "  ./run.sh"
echo "  ./run_improved.sh"
echo "  ./run_fast.sh"
echo "  ./run_realtime.sh"
echo "  ./view_logs.sh" 