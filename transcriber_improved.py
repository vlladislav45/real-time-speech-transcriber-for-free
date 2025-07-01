import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
from datetime import datetime
import os
import json
import time

class ImprovedSpeechTranscriber:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Improved Speech Transcriber")
        self.root.geometry("700x500")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Improved recognition settings
        self.recognizer.energy_threshold = 100  # Lower threshold for better detection
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.5  # Longer pause threshold to catch last word
        self.recognizer.phrase_threshold = 0.1  # Shorter phrase threshold
        self.recognizer.non_speaking_duration = 1.0  # Longer non-speaking duration
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
        # Microphone state management
        self.microphone_in_use = False
        self.microphone_lock = threading.Lock()
        self.listening_thread = None
        
        # State variables
        self.is_listening = False
        self.transcription_queue = queue.Queue()
        
        # Audio buffering for continuous speech
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        self.last_transcription_time = 0
        self.min_buffer_duration = 1.5  # Minimum duration before processing buffer
        
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
        title = tk.Label(self.root, text="Improved Speech Transcriber", font=("Arial", 16))
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
        
        # Refresh button
        refresh_btn = tk.Button(control_frame, text="Refresh", command=self.refresh_microphone)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
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
        
        # Reset microphone state
        with self.microphone_lock:
            self.microphone_in_use = False
        
        # Start listening thread
        self.listening_thread = threading.Thread(target=self.listen_audio, daemon=True)
        self.listening_thread.start()
    
    def stop_listening(self):
        self.is_listening = False
        self.toggle_btn.config(text="Start Listening", bg="#4CAF50", fg="black", 
                              font=("Arial", 10, "bold"))
        self.status_label.config(text="Status: Stopped")
        
        # Reset microphone state
        with self.microphone_lock:
            self.microphone_in_use = False
        
        # Wait for listening thread to finish
        if self.listening_thread and self.listening_thread.is_alive():
            self.listening_thread.join(timeout=2.0)
        
        # Reset listening thread
        self.listening_thread = None
        
        # Save session if we have transcriptions
        if self.current_session and self.current_session["transcriptions"]:
            self.save_session()
    
    def listen_audio(self):
        while self.is_listening:
            try:
                # Use lock to prevent multiple microphone access
                with self.microphone_lock:
                    if self.microphone_in_use:
                        time.sleep(0.1)
                        continue
                    
                    self.microphone_in_use = True
                    
                    try:
                        with self.microphone as source:
                            # Use longer timeout and phrase time limit for continuous speech
                            audio = self.recognizer.listen(
                                source, 
                                timeout=3,  # Longer timeout
                                phrase_time_limit=20,  # Longer phrase time limit
                                snowboy_configuration=None
                            )
                            
                            # Add to buffer instead of immediate processing
                            with self.buffer_lock:
                                self.audio_buffer.append(audio)
                                
                                # Process buffer if it has enough audio
                                if len(self.audio_buffer) >= 2:
                                    self.process_audio_buffer()
                                    
                    finally:
                        self.microphone_in_use = False
                    
            except sr.WaitTimeoutError:
                # Process any remaining audio in buffer
                with self.buffer_lock:
                    if self.audio_buffer:
                        self.process_audio_buffer()
                continue
            except Exception as e:
                print(f"Listening error: {e}")
                # Reset microphone state on error
                with self.microphone_lock:
                    self.microphone_in_use = False
                continue
    
    def start_processing(self):
        # Start buffer processing thread
        threading.Thread(target=self.buffer_processor, daemon=True).start()
        
        # Start checking for transcriptions
        self.check_transcriptions()
    
    def process_audio_buffer(self):
        """Process accumulated audio buffer for better continuous speech recognition"""
        if not self.audio_buffer:
            return
            
        try:
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
            self.status_label.config(text=f"Logs saved in: {self.logs_dir}")
    
    def refresh_microphone(self):
        """Refresh the microphone and reset all states"""
        if self.is_listening:
            # Stop listening first
            self.stop_listening()
            time.sleep(0.5)
        
        # Reset microphone
        self.microphone = sr.Microphone()
        
        # Re-adjust for ambient noise
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Error refreshing microphone: {e}")
        
        # Reset all states
        self.microphone_in_use = False
        self.audio_buffer.clear()
        self.listening_thread = None
        
        # Update status
        self.status_label.config(text="Status: Microphone refreshed")
        
        print("Microphone refreshed successfully")
    
    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImprovedSpeechTranscriber()
    app.run() 