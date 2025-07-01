#!/bin/bash

# Setup Script for Speech Transcriber
# This script sets up the environment and installs dependencies

echo "=== Speech Transcriber Setup ==="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found: $(pip3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✓ Virtual environment created"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."

# Install SpeechRecognition
echo "Installing SpeechRecognition..."
pip install SpeechRecognition
if [ $? -ne 0 ]; then
    echo "❌ Failed to install SpeechRecognition"
    exit 1
fi

# Install PyAudio based on platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS"
    
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "Installing PortAudio via Homebrew..."
        brew install portaudio
        if [ $? -eq 0 ]; then
            echo "✓ PortAudio installed"
        else
            echo "⚠ PortAudio installation failed, but continuing..."
        fi
    else
        echo "⚠ Homebrew not found. You may need to install PortAudio manually."
    fi
    
    echo "Installing PyAudio..."
    pip install pyaudio
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyAudio"
        echo "Try: pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio"
        exit 1
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux"
    echo "You may need to install system dependencies first:"
    echo "sudo apt-get install python3-pyaudio portaudio19-dev"
    
    echo "Installing PyAudio..."
    pip install pyaudio
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyAudio"
        echo "Please install system dependencies first"
        exit 1
    fi
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows
    echo "Detected Windows"
    echo "Installing PyAudio..."
    pip install pyaudio
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyAudio"
        echo "Try: pip install pipwin && pipwin install pyaudio"
        exit 1
    fi
    
else
    echo "Unknown OS: $OSTYPE"
    echo "Installing PyAudio..."
    pip install pyaudio
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyAudio"
        exit 1
    fi
fi

echo "✓ PyAudio installed"

# Create logs directory
if [ ! -d "transcription_logs" ]; then
    echo "Creating logs directory..."
    mkdir transcription_logs
    echo "✓ Logs directory created"
else
    echo "✓ Logs directory already exists"
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x run.sh
chmod +x run_improved.sh
chmod +x run_fast.sh
chmod +x run_realtime.sh
chmod +x view_logs.sh
chmod +x install_global.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "You can now run the speech transcriber:"
echo "  ./run.sh                    # Interactive menu"
echo "  python transcriber.py       # Standard version"
echo "  python transcriber_improved.py  # Improved version"
echo "  python transcriber_fast.py  # Fast version"
echo "  python transcriber_realtime.py  # Real-time version"
echo "  python log_viewer.py        # Log viewer"
echo ""
echo "To test the installation, run:"
echo "  python test_installation.py" 