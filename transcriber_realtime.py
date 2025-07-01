import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
from datetime import datetime
import os
import json
import time
import re

class RealtimeSpeechTranscriber:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real-time Speech Transcriber")
        self.root.geometry("900x700")
        
        # Initialize speech recognition with optimized settings
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Real-time optimized settings
        self.recognizer.energy_threshold = 50  # Very low threshold for immediate detection
        self.recognizer.dynamic_energy_threshold = False  # Disable for faster response
        self.recognizer.pause_threshold = 0.8  # Longer pause to catch last word
        self.recognizer.phrase_threshold = 0.05  # Very short phrase threshold
        self.recognizer.non_speaking_duration = 0.5  # Longer non-speaking duration to catch last word
        
        # Adjust for ambient noise quickly
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Microphone state management
        self.microphone_in_use = False
        self.microphone_lock = threading.Lock()
        self.listening_thread = None  # Track the listening thread
        
        # State variables
        self.is_listening = False
        self.transcription_queue = queue.Queue()
        self.current_text = ""
        self.last_processed_text = ""
        
        # Create logs directory
        self.logs_dir = "transcription_logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        # Initialize current session
        self.current_session = None
        self.session_start_time = None
        
        # Performance tracking
        self.transcription_count = 0
        self.word_count = 0
        
        # Real-time display
        self.current_display_text = ""
        self.is_processing = False
        self.is_actively_listening = False  # Track if we're actively listening
        self.last_audio_time = 0  # Track when we last got audio
        self.phrase_buffer = ""  # Buffer for incomplete phrases
        
        self.setup_gui()
        self.start_processing()
    
    def setup_gui(self):
        # Title
        title = tk.Label(self.root, text="Real-time Speech Transcriber", font=("Arial", 16))
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
        
        # Performance label
        self.perf_label = tk.Label(control_frame, text="Words: 0 | Phrases: 0")
        self.perf_label.pack(side=tk.RIGHT, padx=10)
        
        # Real-time display frame
        realtime_frame = tk.Frame(self.root)
        realtime_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Real-time label
        tk.Label(realtime_frame, text="Real-time:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Real-time text area (smaller, for current phrase)
        self.realtime_text = tk.Text(realtime_frame, height=3, font=("Arial", 12, "italic"), 
                                    bg="#f0f8ff", fg="#0066cc", wrap=tk.WORD)
        self.realtime_text.pack(fill=tk.X, pady=(5, 10))
        
        # Final transcriptions label
        tk.Label(realtime_frame, text="Final Transcriptions:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Final transcriptions display
        self.text_area = scrolledtext.ScrolledText(self.root, height=15, width=80, font=("Arial", 12))
        self.text_area.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = "Click 'Start Listening' to begin. Words appear in real-time as you speak."
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
        
        # Reset tracking
        self.transcription_count = 0
        self.word_count = 0
        self.current_text = ""
        self.last_processed_text = ""
        self.is_actively_listening = False
        self.last_audio_time = 0
        self.phrase_buffer = ""
        self.microphone_in_use = False
        self.listening_thread = None
        self.perf_label.config(text="Words: 0 | Phrases: 0")
        
        # Clear displays
        self.realtime_text.delete(1.0, tk.END)
        self.current_display_text = ""
        
        # Start listening thread
        self.listening_thread = threading.Thread(target=self.realtime_listen, daemon=True)
        self.listening_thread.start()
    
    def stop_listening(self):
        self.is_listening = False
        self.toggle_btn.config(text="Start Listening", bg="#4CAF50", fg="black", 
                              font=("Arial", 10, "bold"))
        self.status_label.config(text="Status: Stopped")
        
        # Clear real-time display
        self.realtime_text.delete(1.0, tk.END)
        
        # Reset microphone state
        with self.microphone_lock:
            self.microphone_in_use = False
        
        # Wait for listening thread to finish
        if self.listening_thread and self.listening_thread.is_alive():
            self.listening_thread.join(timeout=2.0)  # Wait up to 2 seconds
        
        # Reset listening thread
        self.listening_thread = None
        
        # Save session if we have transcriptions
        if self.current_session and self.current_session["transcriptions"]:
            self.save_session()
    
    def realtime_listen(self):
        """Real-time listening with word-by-word display"""
        # Reset microphone state at start
        with self.microphone_lock:
            self.microphone_in_use = False
        
        while self.is_listening:
            try:
                # Use lock to prevent multiple microphone access
                with self.microphone_lock:
                    if self.microphone_in_use:
                        time.sleep(0.1)  # Wait a bit if microphone is in use
                        continue
                    
                    self.microphone_in_use = True
                    
                    try:
                        with self.microphone as source:
                            # Use longer timeout to catch last word
                            audio = self.recognizer.listen(
                                source, 
                                timeout=1.0,  # Longer timeout to catch last word
                                phrase_time_limit=8,  # Longer phrase time to catch complete sentences
                                snowboy_configuration=None
                            )
                            
                            # Mark as actively listening when we get audio
                            self.is_actively_listening = True
                            self.last_audio_time = time.time()
                            
                            # Process immediately
                            threading.Thread(target=self.process_audio_realtime, args=(audio,), daemon=True).start()
                            
                    finally:
                        self.microphone_in_use = False
                    
            except sr.WaitTimeoutError:
                # Check if we should process any buffered text
                current_time = time.time()
                if self.is_actively_listening and self.phrase_buffer and (current_time - self.last_audio_time) > 1.0:
                    # Process any remaining buffered text
                    self.process_buffered_text()
                
                # Update status to show it's still listening
                if not self.is_actively_listening:
                    self.root.after(0, lambda: self.status_label.config(text="Status: Listening... (waiting)"))
                else:
                    self.root.after(0, lambda: self.status_label.config(text="Status: Listening... (active)"))
                continue
            except Exception as e:
                print(f"Listening error: {e}")
                # Reset microphone state on error
                with self.microphone_lock:
                    self.microphone_in_use = False
                # Small delay to prevent rapid error loops
                time.sleep(0.1)
                continue
    
    def process_audio_realtime(self, audio):
        """Process audio with real-time word display"""
        try:
            # Show processing status
            self.root.after(0, lambda: self.status_label.config(text="Status: Processing..."))
            
            text = self.recognizer.recognize_google(audio)
            if text.strip():
                # Add to phrase buffer
                if self.phrase_buffer:
                    self.phrase_buffer += " " + text
                else:
                    self.phrase_buffer = text
                
                # Update real-time display
                self.update_realtime_display(self.phrase_buffer)
                
                # Check if this looks like a complete phrase (ends with punctuation or is long enough)
                if self.is_complete_phrase(text):
                    # Process the complete phrase
                    self.process_complete_phrase()
                
                # Update status to show we're actively listening
                self.root.after(0, lambda: self.status_label.config(text="Status: Listening... (active)"))
                
        except sr.UnknownValueError:
            # Update status back to listening
            self.root.after(0, lambda: self.status_label.config(text="Status: Listening... (active)"))
        except sr.RequestError as e:
            print(f"Recognition error: {e}")
            self.root.after(0, lambda: self.status_label.config(text="Status: Network Error"))
        except Exception as e:
            print(f"Processing error: {e}")
            self.root.after(0, lambda: self.status_label.config(text="Status: Error"))
    
    def is_complete_phrase(self, text):
        """Check if the text looks like a complete phrase"""
        # Ends with punctuation
        if text.strip().endswith(('.', '!', '?', ':', ';')):
            return True
        
        # Is a long enough phrase (more than 5 words)
        if len(text.split()) >= 5:
            return True
        
        # Has been buffered for a while (will be handled by timeout)
        return False
    
    def process_complete_phrase(self):
        """Process a complete phrase from the buffer"""
        if not self.phrase_buffer.strip():
            return
            
        # Add to final transcriptions
        timestamp = datetime.now().strftime("%H:%M:%S")
        transcription_entry = f"[{timestamp}] {self.phrase_buffer}"
        self.transcription_queue.put(transcription_entry)
        
        # Update counters
        self.transcription_count += 1
        words_in_phrase = len(self.phrase_buffer.split())
        self.word_count += words_in_phrase
        
        self.root.after(0, lambda: self.perf_label.config(
            text=f"Words: {self.word_count} | Phrases: {self.transcription_count}"))
        
        # Add to current session
        if self.current_session:
            self.current_session["transcriptions"].append({
                "timestamp": timestamp,
                "text": self.phrase_buffer,
                "full_entry": transcription_entry,
                "word_count": words_in_phrase
            })
        
        # Clear the buffer
        self.phrase_buffer = ""
    
    def process_buffered_text(self):
        """Process any remaining text in the buffer"""
        if self.phrase_buffer.strip():
            self.process_complete_phrase()
    
    def update_realtime_display(self, new_text):
        """Update the real-time display with new text"""
        # Add new text to current display
        if self.current_display_text:
            self.current_display_text += " " + new_text
        else:
            self.current_display_text = new_text
        
        # Update the real-time text area
        self.root.after(0, lambda: self.realtime_text.delete(1.0, tk.END))
        self.root.after(0, lambda: self.realtime_text.insert(1.0, self.current_display_text))
        
        # Auto-scroll to end
        self.root.after(0, lambda: self.realtime_text.see(tk.END))
        
        # Clear real-time display after a short delay (simulates word-by-word)
        self.root.after(2000, self.clear_realtime_display)
    
    def clear_realtime_display(self):
        """Clear the real-time display after processing"""
        if self.is_listening:
            self.current_display_text = ""
            self.realtime_text.delete(1.0, tk.END)
    
    def start_processing(self):
        # Start checking for transcriptions
        self.check_transcriptions()
    
    def check_transcriptions(self):
        """Check for new transcriptions and update display"""
        try:
            while True:
                transcription = self.transcription_queue.get_nowait()
                self.text_area.insert(tk.END, transcription + "\n")
                self.text_area.see(tk.END)
                
                # Force update the display
                self.text_area.update_idletasks()
        except queue.Empty:
            pass
        
        # Check frequently for real-time feel
        self.root.after(50, self.check_transcriptions)
    
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
        self.current_session["total_transcriptions"] = self.transcription_count
        self.current_session["total_words"] = self.word_count
        
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
            time.sleep(0.5)  # Wait a bit
        
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
        self.is_actively_listening = False
        self.phrase_buffer = ""
        self.current_display_text = ""
        self.listening_thread = None
        
        # Update status
        self.status_label.config(text="Status: Microphone refreshed")
        
        print("Microphone refreshed successfully")
    
    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
        self.realtime_text.delete(1.0, tk.END)
        self.current_display_text = ""
        self.phrase_buffer = ""
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RealtimeSpeechTranscriber()
    app.run() 