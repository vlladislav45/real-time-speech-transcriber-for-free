#!/usr/bin/env python3
"""
Version Switcher for Speech Transcriber
This script helps you choose and run different versions of the speech transcriber
"""

import os
import sys
import subprocess
import time

def print_menu():
    """Print the main menu"""
    print("=== Speech Transcriber ===")
    print()
    print("Choose a version to run:")
    print("1. Standard Version (transcriber.py)")
    print("2. Improved Version (transcriber_improved.py)")
    print("3. Fast Version (transcriber_fast.py)")
    print("4. Real-time Version (transcriber_realtime.py)")
    print("5. Log Viewer (log_viewer.py)")
    print("6. Exit")
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import speech_recognition
        import pyaudio
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install dependencies using:")
        print("  pip install -r requirements.txt")
        return False

def run_version(version_num):
    """Run the selected version"""
    version_map = {
        1: ("Standard Version", "transcriber.py"),
        2: ("Improved Version", "transcriber_improved.py"),
        3: ("Fast Version", "transcriber_fast.py"),
        4: ("Real-time Version", "transcriber_realtime.py"),
        5: ("Log Viewer", "log_viewer.py")
    }
    
    if version_num not in version_map:
        print("Invalid option. Please choose 1-6.")
        return
    
    name, filename = version_map[version_num]
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return
    
    print(f"Starting {name}...")
    print()
    
    try:
        # Run the selected version
        subprocess.run([sys.executable, filename])
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error running {name}: {e}")

def main():
    """Main function"""
    # Check dependencies first
    if not check_dependencies():
        return
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "6":
                print("Exiting...")
                break
            elif choice in ["1", "2", "3", "4", "5"]:
                run_version(int(choice))
                print()
                input("Press Enter to continue...")
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main() 