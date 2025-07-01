import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
from datetime import datetime
import os
import json

class SpeechTranscriber:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speech Transcriber")
        self.root.geometry("700x500")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configure recognition settings for better detection
        self.recognizer.energy_threshold = 200  # Even lower threshold for better detection
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.2  # Longer pause threshold to capture more words
        self.recognizer.phrase_threshold = 0.1  # Very short phrase threshold
        self.recognizer.non_speaking_duration = 0.8  # Longer non-speaking duration
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
        # State variables
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.transcription_queue = queue.Queue()
        
        # Audio buffering for continuous speech
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        self.last_transcription_time = 0
        self.min_buffer_duration = 2.0  # Minimum duration before processing buffer
        
        # Create logs directory
        self.logs_dir = "transcription_logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        # Initialize current session
        self.current_session = None
        self.session_start_time = None
        
        self.setup_gui()
        self.start_processing()
    
    def setup_gui(self):
        # Title
        title = tk.Label(self.root, text="Real-Time Speech Transcriber", font=("Arial", 16))
        title.pack(pady=10)
        
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        
        # Start/Stop button
        self.toggle_btn = tk.Button(control_frame, text="Start Listening", 
                                   command=self.toggle_listening, bg="#4CAF50", fg="black", 
                                   font=("Arial", 10, "bold"), relief=tk.RAISED, bd=2)
        self.toggle_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(control_frame, text="Clear Text", command=self.clear_text)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # View logs button
        logs_btn = tk.Button(control_frame, text="View Logs", command=self.view_logs)
        logs_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Status: Ready")
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Text display
        self.text_area = scrolledtext.ScrolledText(self.root, height=20, width=80, font=("Arial", 12))
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = "Click 'Start Listening' to begin transcription. Speak clearly into your microphone."
        tk.Label(self.root, text=instructions, fg="gray").pack(pady=5)
    
    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        self.is_listening = True
        self.toggle_btn.config(text="Stop Listening", bg="#f44336", fg="black", 
                              font=("Arial", 10, "bold"))
        self.status_label.config(text="Status: Listening...")
        
        # Start new session
        self.session_start_time = datetime.now()
        self.current_session = {
            "start_time": self.session_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "transcriptions": []
        }
        
        # Start listening thread
        threading.Thread(target=self.listen_audio, daemon=True).start()
    
    def stop_listening(self):
        self.is_listening = False
        self.toggle_btn.config(text="Start Listening", bg="#4CAF50", fg="black", 
                              font=("Arial", 10, "bold"))
        self.status_label.config(text="Status: Stopped")
        
        # Save session if we have transcriptions
        if self.current_session and self.current_session["transcriptions"]:
            self.save_session()
    
    def listen_audio(self):
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Use longer timeout and phrase time limit for continuous speech
                    audio = self.recognizer.listen(
                        source, 
                        timeout=5,  # Longer timeout
                        phrase_time_limit=30,  # Much longer phrase time limit
                        snowboy_configuration=None  # Disable snowboy for better compatibility
                    )
                    
                    # Add to buffer instead of immediate processing
                    with self.buffer_lock:
                        self.audio_buffer.append(audio)
                        
                        # Process buffer if it has enough audio
                        if len(self.audio_buffer) >= 2:  # Process when we have multiple audio chunks
                            self.process_audio_buffer()
                            
            except sr.WaitTimeoutError:
                # Process any remaining audio in buffer
                with self.buffer_lock:
                    if self.audio_buffer:
                        self.process_audio_buffer()
                continue
            except Exception as e:
                print(f"Listening error: {e}")
                continue
    
    def start_processing(self):
        # Start audio processing thread
        threading.Thread(target=self.process_audio, daemon=True).start()
        
        # Start buffer processing thread
        threading.Thread(target=self.buffer_processor, daemon=True).start()
        
        # Start checking for transcriptions
        self.check_transcriptions()
    
    def process_audio(self):
        """Legacy audio processing - kept for compatibility"""
        while True:
            try:
                audio = self.audio_queue.get(timeout=1)
                self.process_single_audio(audio)
            except queue.Empty:
                continue
    
    def process_audio_buffer(self):
        """Process accumulated audio buffer for better continuous speech recognition"""
        if not self.audio_buffer:
            return
            
        try:
            # Combine multiple audio chunks for better recognition
            combined_audio = self.audio_buffer[0]
            for audio_chunk in self.audio_buffer[1:]:
                # Combine audio data (this is a simplified approach)
                # In practice, we'll process each chunk separately but in sequence
                pass
            
            # Process each audio chunk in the buffer
            for audio in self.audio_buffer:
                self.process_single_audio(audio)
                
            # Clear the buffer
            self.audio_buffer.clear()
            
        except Exception as e:
            print(f"Error processing audio buffer: {e}")
            self.audio_buffer.clear()
    
    def process_single_audio(self, audio):
        """Process a single audio chunk"""
        try:
            text = self.recognizer.recognize_google(audio)
            if text.strip():
                timestamp = datetime.now().strftime("%H:%M:%S")
                transcription_entry = f"[{timestamp}] {text}"
                self.transcription_queue.put(transcription_entry)
                
                # Add to current session
                if self.current_session:
                    self.current_session["transcriptions"].append({
                        "timestamp": timestamp,
                        "text": text,
                        "full_entry": transcription_entry
                    })
                    
        except sr.UnknownValueError:
            # Speech was unintelligible
            pass
        except sr.RequestError as e:
            print(f"Recognition error: {e}")
    
    def buffer_processor(self):
        """Background thread to process audio buffer periodically"""
        import time
        
        while True:
            time.sleep(1)  # Check every second
            
            if not self.is_listening:
                continue
                
            with self.buffer_lock:
                if self.audio_buffer and len(self.audio_buffer) >= 1:
                    # Process buffer if it has been sitting for a while
                    current_time = time.time()
                    if current_time - self.last_transcription_time > self.min_buffer_duration:
                        self.process_audio_buffer()
                        self.last_transcription_time = current_time
    
    def check_transcriptions(self):
        """Check for new transcriptions and update display"""
        try:
            while True:
                transcription = self.transcription_queue.get_nowait()
                self.text_area.insert(tk.END, transcription + "\n")
                self.text_area.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_transcriptions)
    
    def save_session(self):
        """Save the current session to a log file"""
        if not self.current_session or not self.current_session["transcriptions"]:
            return
            
        # Create filename based on date and time
        date_str = self.session_start_time.strftime("%Y-%m-%d")
        time_str = self.session_start_time.strftime("%H-%M-%S")
        filename = f"transcription_{date_str}_{time_str}.json"
        filepath = os.path.join(self.logs_dir, filename)
        
        # Add end time
        end_time = datetime.now()
        self.current_session["end_time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
        self.current_session["duration_minutes"] = (end_time - self.session_start_time).total_seconds() / 60
        
        # Save as JSON
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.current_session, f, indent=2, ensure_ascii=False)
            print(f"Session saved to: {filepath}")
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def view_logs(self):
        """Open the logs directory in file explorer"""
        import subprocess
        import platform
        
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.logs_dir])
            elif platform.system() == "Windows":
                subprocess.run(["explorer", self.logs_dir])
            else:  # Linux
                subprocess.run(["xdg-open", self.logs_dir])
        except Exception as e:
            print(f"Error opening logs directory: {e}")
            # Fallback: show path in status
            self.status_label.config(text=f"Logs saved in: {self.logs_dir}")
    
    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SpeechTranscriber()
    app.run() 