# Quick Start Guide

## Installation

### Option 1: Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Global Installation (macOS)

```bash
# Install system dependencies
brew install portaudio python@3.11

# Install Python packages
pip3 install SpeechRecognition pyaudio
```

## Running the Application

### Quick Start (Interactive Menu)
```bash
./run.sh
```

### Individual Versions

**Standard Version:**
```bash
python transcriber.py
```

**Improved Version (Recommended for meetings):**
```bash
python transcriber_improved.py
```

**Fast Version:**
```bash
python transcriber_fast.py
```

**Real-time Version:**
```bash
python transcriber_realtime.py
```

**Log Viewer:**
```bash
python log_viewer.py
```

## Usage

1. **Start the application** using one of the commands above
2. **Click "Start Listening"** to begin transcription
3. **Speak clearly** into your microphone
4. **Click "Stop Listening"** when finished
5. **View logs** using the "View Logs" button

## Tips for Best Results

- **Use the improved version** for meetings and continuous speech
- **Speak clearly** and at a normal pace
- **Minimize background noise**
- **Ensure good microphone positioning**
- **Use the "Refresh" button** if you have microphone issues

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

2. **Microphone not working**
   - Check microphone permissions in System Preferences
   - Try the "Refresh" button in the application
   - Restart the application

3. **Poor transcription quality**
   - Speak clearly and at a normal pace
   - Reduce background noise
   - Try different versions

## File Locations

- **Transcription logs**: `transcription_logs/` directory
- **Log files**: JSON format with timestamps
- **Export**: Use the log viewer to export to text files

## 🎯 Perfect For
- Meeting notes
- Interview transcriptions  
- Voice memos
- Accessibility support
- Language learning

## 💡 Tips for Best Results
- Speak clearly and at normal pace
- Minimize background noise
- Keep microphone close to your mouth
- Ensure stable internet connection

## 🔧 Troubleshooting
If you get errors:
1. Make sure microphone permissions are enabled
2. Check internet connection
3. Try running `./run.sh` again

## 📱 Features
- ✅ Real-time transcription
- ✅ Automatic logging to files
- ✅ Log viewer with search
- ✅ Timestamped entries
- ✅ Export functionality
- ✅ Simple GUI interface
- ✅ Free to use
- ✅ Works offline (after initial setup) 