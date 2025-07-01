#!/usr/bin/env python3
"""
Log Viewer for Speech Transcriber
View and search through transcription logs
"""

import json
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from datetime import datetime
import glob

class LogViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Transcription Log Viewer")
        self.root.geometry("1000x700")
        
        # Data storage
        self.logs_dir = "transcription_logs"
        self.log_files = []
        self.current_log_data = None
        
        self.setup_gui()
        self.load_log_files()
    
    def setup_gui(self):
        # Title
        title = tk.Label(self.root, text="Transcription Log Viewer", font=("Arial", 16))
        title.pack(pady=10)
        
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5, fill=tk.X, padx=10)
        
        # Log file selection
        tk.Label(control_frame, text="Select Log File:").pack(side=tk.LEFT)
        
        self.log_var = tk.StringVar()
        self.log_dropdown = ttk.Combobox(control_frame, textvariable=self.log_var, width=50)
        self.log_dropdown.pack(side=tk.LEFT, padx=5)
        self.log_dropdown.bind('<<ComboboxSelected>>', self.on_log_selected)
        
        # Refresh button
        refresh_btn = tk.Button(control_frame, text="Refresh", command=self.load_log_files)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        export_btn = tk.Button(control_frame, text="Export", command=self.export_log)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5, fill=tk.X, padx=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_var.trace('w', self.on_search_changed)
        
        # Clear search button
        clear_search_btn = tk.Button(search_frame, text="Clear Search", command=self.clear_search)
        clear_search_btn.pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.stats_label = tk.Label(stats_frame, text="No log selected", font=("Arial", 10))
        self.stats_label.pack(anchor=tk.W)
        
        # Content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Transcriptions display
        self.text_area = scrolledtext.ScrolledText(content_frame, font=("Arial", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True)
    
    def load_log_files(self):
        """Load all JSON log files from the logs directory"""
        try:
            if not os.path.exists(self.logs_dir):
                messagebox.showwarning("Warning", f"Logs directory '{self.logs_dir}' not found.")
                return
            
            # Find all JSON files
            pattern = os.path.join(self.logs_dir, "*.json")
            self.log_files = glob.glob(pattern)
            
            # Create display names for dropdown
            display_names = []
            for file_path in self.log_files:
                filename = os.path.basename(file_path)
                # Try to extract date and time from filename
                if filename.startswith("transcription_"):
                    # Remove "transcription_" prefix and ".json" suffix
                    date_time_part = filename[14:-5]  # Remove "transcription_" and ".json"
                    try:
                        # Parse the date and time
                        dt = datetime.strptime(date_time_part, "%Y-%m-%d_%H-%M-%S")
                        display_name = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        display_name = filename
                else:
                    display_name = filename
                display_names.append(display_name)
            
            # Update dropdown
            self.log_dropdown['values'] = display_names
            
            if display_names:
                self.log_dropdown.set(display_names[0])  # Select first log
                self.on_log_selected(None)
            else:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, "No log files found in the transcription_logs directory.")
                self.stats_label.config(text="No logs available")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading log files: {e}")
    
    def on_log_selected(self, event):
        """Handle log file selection"""
        try:
            selected_index = self.log_dropdown.current()
            if selected_index >= 0 and selected_index < len(self.log_files):
                file_path = self.log_files[selected_index]
                self.load_log_content(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading log: {e}")
    
    def load_log_content(self, file_path):
        """Load and display log content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_log_data = json.load(f)
            
            # Display content
            self.display_log_content()
            
            # Update statistics
            self.update_statistics()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error reading log file: {e}")
            self.current_log_data = None
    
    def display_log_content(self):
        """Display the log content in the text area"""
        if not self.current_log_data:
            return
        
        self.text_area.delete(1.0, tk.END)
        
        # Display session info
        session_info = f"Session Information:\n"
        session_info += f"Start Time: {self.current_log_data.get('start_time', 'Unknown')}\n"
        session_info += f"End Time: {self.current_log_data.get('end_time', 'Unknown')}\n"
        session_info += f"Duration: {self.current_log_data.get('duration_minutes', 0):.1f} minutes\n"
        session_info += f"Total Transcriptions: {len(self.current_log_data.get('transcriptions', []))}\n"
        
        # Add word count if available
        total_words = 0
        for trans in self.current_log_data.get('transcriptions', []):
            if 'word_count' in trans:
                total_words += trans['word_count']
            else:
                # Estimate word count
                total_words += len(trans.get('text', '').split())
        
        session_info += f"Total Words: {total_words}\n"
        session_info += "-" * 50 + "\n\n"
        
        self.text_area.insert(tk.END, session_info)
        
        # Display transcriptions
        transcriptions = self.current_log_data.get('transcriptions', [])
        for trans in transcriptions:
            if 'full_entry' in trans:
                self.text_area.insert(tk.END, trans['full_entry'] + "\n")
            else:
                # Fallback for older format
                timestamp = trans.get('timestamp', 'Unknown')
                text = trans.get('text', '')
                self.text_area.insert(tk.END, f"[{timestamp}] {text}\n")
    
    def update_statistics(self):
        """Update the statistics display"""
        if not self.current_log_data:
            self.stats_label.config(text="No log selected")
            return
        
        transcriptions = self.current_log_data.get('transcriptions', [])
        total_words = 0
        for trans in transcriptions:
            if 'word_count' in trans:
                total_words += trans['word_count']
            else:
                total_words += len(trans.get('text', '').split())
        
        duration = self.current_log_data.get('duration_minutes', 0)
        words_per_minute = total_words / duration if duration > 0 else 0
        
        stats_text = f"Transcriptions: {len(transcriptions)} | Words: {total_words} | Duration: {duration:.1f} min | WPM: {words_per_minute:.1f}"
        self.stats_label.config(text=stats_text)
    
    def on_search_changed(self, *args):
        """Handle search text changes"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.display_log_content()
            return
        
        if not self.current_log_data:
            return
        
        # Filter transcriptions based on search term
        filtered_transcriptions = []
        for trans in self.current_log_data.get('transcriptions', []):
            text = trans.get('text', '').lower()
            if search_term in text:
                filtered_transcriptions.append(trans)
        
        # Display filtered content
        self.text_area.delete(1.0, tk.END)
        
        if filtered_transcriptions:
            self.text_area.insert(tk.END, f"Search Results for '{search_term}' ({len(filtered_transcriptions)} matches):\n")
            self.text_area.insert(tk.END, "-" * 50 + "\n\n")
            
            for trans in filtered_transcriptions:
                if 'full_entry' in trans:
                    self.text_area.insert(tk.END, trans['full_entry'] + "\n")
                else:
                    timestamp = trans.get('timestamp', 'Unknown')
                    text = trans.get('text', '')
                    self.text_area.insert(tk.END, f"[{timestamp}] {text}\n")
        else:
            self.text_area.insert(tk.END, f"No matches found for '{search_term}'")
    
    def clear_search(self):
        """Clear the search and show all content"""
        self.search_var.set("")
        self.display_log_content()
    
    def export_log(self):
        """Export the current log to a text file"""
        if not self.current_log_data:
            messagebox.showwarning("Warning", "No log selected for export.")
            return
        
        try:
            # Get save file path
            filename = f"exported_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialname=filename
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Write session info
                    f.write("Session Information:\n")
                    f.write(f"Start Time: {self.current_log_data.get('start_time', 'Unknown')}\n")
                    f.write(f"End Time: {self.current_log_data.get('end_time', 'Unknown')}\n")
                    f.write(f"Duration: {self.current_log_data.get('duration_minutes', 0):.1f} minutes\n")
                    f.write(f"Total Transcriptions: {len(self.current_log_data.get('transcriptions', []))}\n")
                    f.write("-" * 50 + "\n\n")
                    
                    # Write transcriptions
                    for trans in self.current_log_data.get('transcriptions', []):
                        if 'full_entry' in trans:
                            f.write(trans['full_entry'] + "\n")
                        else:
                            timestamp = trans.get('timestamp', 'Unknown')
                            text = trans.get('text', '')
                            f.write(f"[{timestamp}] {text}\n")
                
                messagebox.showinfo("Success", f"Log exported to: {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting log: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LogViewer()
    app.run() 