# Speech Transcriber

A real-time speech-to-text transcription application for macOS (M2 Silicon) with multiple versions optimized for different use cases.

## Features

- **Real-time transcription** using Google Speech Recognition API
- **Multiple versions** optimized for different scenarios:
  - Standard version: Balanced performance
  - Improved version: Better continuous speech handling
  - Fast version: Quick response times
  - Real-time version: Word-by-word display
- **Automatic logging** of all transcription sessions
- **Log viewer** with search and export capabilities
- **Thread-safe microphone handling** with proper cleanup
- **Cross-platform compatibility** (primarily tested on macOS)

## Installation

### Option 1: Using Virtual Environment (Recommended)

1. **Clone or download the project**
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PyAudio (if needed):**
   ```bash
   # On macOS with Homebrew:
   brew install portaudio
   pip install pyaudio
   
   # Or using conda:
   conda install pyaudio
   ```

### Option 2: Global Installation (macOS)

1. **Install Homebrew dependencies:**
   ```bash
   brew install portaudio python@3.11
   ```

2. **Install Python packages globally:**
   ```bash
   pip3 install SpeechRecognition pyaudio
   ```

## Usage

### Running Different Versions

The application comes with multiple versions optimized for different use cases:

#### 1. Standard Version
```bash
python transcriber.py
```
- Balanced performance
- Good for general use
- Automatic session logging

#### 2. Improved Version
```bash
python transcriber_improved.py
```
- Better continuous speech handling
- Audio buffering for improved accuracy
- Reduced missed words

#### 3. Fast Version
```bash
python transcriber_fast.py
```
- Optimized for quick response
- Lower latency
- Good for quick notes

#### 4. Real-time Version
```bash
python transcriber_realtime.py
```
- Word-by-word real-time display
- Live transcription feedback
- Performance tracking

### Using the Application

1. **Start the application** using one of the commands above
2. **Click "Start Listening"** to begin transcription
3. **Speak clearly** into your microphone
4. **Click "Stop Listening"** when finished
5. **View logs** using the "View Logs" button

### Log Viewer

The log viewer allows you to:
- Browse all transcription sessions
- Search through transcriptions
- Export sessions to text files
- View session statistics

```bash
python log_viewer.py
```

## File Structure

```
transcribe-speech-to-text/
├── transcriber.py              # Standard version
├── transcriber_improved.py     # Improved version
├── transcriber_fast.py         # Fast version
├── transcriber_realtime.py     # Real-time version
├── log_viewer.py              # Log viewer application
├── requirements.txt           # Python dependencies
├── transcription_logs/        # Session logs (auto-created)
└── README.md                 # This file
```

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   - Install portaudio: `brew install portaudio`
   - Then install pyaudio: `pip install pyaudio`

2. **Microphone not working**
   - Check microphone permissions in System Preferences
   - Try the "Refresh" button in the application
   - Restart the application

3. **Poor transcription quality**
   - Speak clearly and at a normal pace
   - Reduce background noise
   - Try different versions (improved or real-time)

4. **"Listening timed out" errors**
   - This is normal when no speech is detected
   - The application will continue listening
   - Try the improved version for better handling

### Performance Tips

- Use the **improved version** for continuous speech
- Use the **fast version** for quick notes
- Use the **real-time version** for live feedback
- Ensure good microphone quality and positioning
- Minimize background noise

## Technical Details

### Recognition Settings

Each version uses different recognition parameters:

- **Energy Threshold**: Sensitivity to speech (lower = more sensitive)
- **Pause Threshold**: How long to wait after speech ends
- **Phrase Threshold**: Minimum duration for a phrase
- **Non-speaking Duration**: How long to wait for more speech

### Logging Format

Sessions are saved as JSON files with:
- Session metadata (start/end times, duration)
- Individual transcriptions with timestamps
- Word counts and performance metrics

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Try different versions of the application
3. Ensure your microphone and internet connection are working properly 