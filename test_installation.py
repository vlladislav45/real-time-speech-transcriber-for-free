#!/usr/bin/env python3
"""
Test Installation Script for Speech Transcriber
This script tests if all dependencies are properly installed
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    modules_to_test = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "PyAudio"),
        ("tkinter", "Tkinter"),
        ("json", "JSON"),
        ("threading", "Threading"),
        ("queue", "Queue"),
        ("datetime", "Datetime")
    ]
    
    failed_imports = []
    
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {display_name}")
        except ImportError as e:
            print(f"✗ {display_name}: {e}")
            failed_imports.append(module_name)
    
    return failed_imports

def test_microphone():
    """Test if microphone is accessible"""
    print("\nTesting microphone access...")
    
    try:
        import speech_recognition as sr
        mic = sr.Microphone()
        
        # Try to get microphone info
        with mic as source:
            print("✓ Microphone detected")
            print(f"  Device: {mic.device_index}")
            print(f"  Sample rate: {source.SAMPLE_RATE}")
            print(f"  Chunk size: {source.CHUNK}")
            return True
    except Exception as e:
        print(f"✗ Microphone error: {e}")
        return False

def test_speech_recognition():
    """Test if speech recognition is working"""
    print("\nTesting speech recognition...")
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        # Test with a simple audio recognition (this won't actually recognize anything)
        # but it will test if the recognizer can be created
        print("✓ Speech recognition initialized")
        print(f"  Energy threshold: {recognizer.energy_threshold}")
        print(f"  Pause threshold: {recognizer.pause_threshold}")
        return True
    except Exception as e:
        print(f"✗ Speech recognition error: {e}")
        return False

def test_gui():
    """Test if GUI can be created"""
    print("\nTesting GUI...")
    
    try:
        import tkinter as tk
        
        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test basic GUI elements
        label = tk.Label(root, text="Test")
        button = tk.Button(root, text="Test")
        
        root.destroy()
        print("✓ GUI components working")
        return True
    except Exception as e:
        print(f"✗ GUI error: {e}")
        return False

def test_files():
    """Test if all required files exist"""
    print("\nTesting files...")
    
    required_files = [
        "transcriber.py",
        "transcriber_improved.py", 
        "transcriber_fast.py",
        "transcriber_realtime.py",
        "log_viewer.py",
        "requirements.txt"
    ]
    
    missing_files = []
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} (missing)")
            missing_files.append(filename)
    
    return missing_files

def test_logs_directory():
    """Test if logs directory exists and is writable"""
    print("\nTesting logs directory...")
    
    logs_dir = "transcription_logs"
    
    if not os.path.exists(logs_dir):
        try:
            os.makedirs(logs_dir)
            print(f"✓ Created {logs_dir} directory")
        except Exception as e:
            print(f"✗ Could not create {logs_dir}: {e}")
            return False
    else:
        print(f"✓ {logs_dir} directory exists")
    
    # Test if directory is writable
    try:
        test_file = os.path.join(logs_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✓ Directory is writable")
        return True
    except Exception as e:
        print(f"✗ Directory not writable: {e}")
        return False

def main():
    """Main test function"""
    print("=== Speech Transcriber Installation Test ===")
    print()
    
    # Test imports
    failed_imports = test_imports()
    
    # Test microphone
    mic_ok = test_microphone()
    
    # Test speech recognition
    sr_ok = test_speech_recognition()
    
    # Test GUI
    gui_ok = test_gui()
    
    # Test files
    missing_files = test_files()
    
    # Test logs directory
    logs_ok = test_logs_directory()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    if not failed_imports and not missing_files and mic_ok and sr_ok and gui_ok and logs_ok:
        print("🎉 ALL TESTS PASSED!")
        print("Your installation is ready to use.")
        print("\nYou can now run:")
        print("  python transcriber.py")
        print("  python transcriber_improved.py")
        print("  python transcriber_fast.py")
        print("  python transcriber_realtime.py")
        print("  python log_viewer.py")
        print("  ./run.sh")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nIssues found:")
        
        if failed_imports:
            print(f"  - Missing imports: {', '.join(failed_imports)}")
            print("    Solution: pip install -r requirements.txt")
        
        if missing_files:
            print(f"  - Missing files: {', '.join(missing_files)}")
            print("    Solution: Make sure all files are in the current directory")
        
        if not mic_ok:
            print("  - Microphone not accessible")
            print("    Solution: Check microphone permissions and connections")
        
        if not sr_ok:
            print("  - Speech recognition not working")
            print("    Solution: Check internet connection and API access")
        
        if not gui_ok:
            print("  - GUI not working")
            print("    Solution: Check tkinter installation")
        
        if not logs_ok:
            print("  - Logs directory not writable")
            print("    Solution: Check directory permissions")
        
        print("\nPlease fix the issues above and run this test again.")

if __name__ == "__main__":
    main() 