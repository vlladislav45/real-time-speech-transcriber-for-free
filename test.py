#!/usr/bin/env python3
"""
Simple Test Script for Speech Transcriber
Quick test to verify basic functionality
"""

import sys
import os

def quick_test():
    """Quick test of basic functionality"""
    print("=== Quick Test ===")
    
    # Test imports
    try:
        import speech_recognition as sr
        print("✓ SpeechRecognition imported")
    except ImportError:
        print("✗ SpeechRecognition not found")
        return False
    
    try:
        import pyaudio
        print("✓ PyAudio imported")
    except ImportError:
        print("✗ PyAudio not found")
        return False
    
    try:
        import tkinter as tk
        print("✓ Tkinter imported")
    except ImportError:
        print("✗ Tkinter not found")
        return False
    
    # Test microphone
    try:
        mic = sr.Microphone()
        print("✓ Microphone detected")
    except Exception as e:
        print(f"✗ Microphone error: {e}")
        return False
    
    # Test recognizer
    try:
        recognizer = sr.Recognizer()
        print("✓ Speech recognizer created")
    except Exception as e:
        print(f"✗ Recognizer error: {e}")
        return False
    
    # Test files
    required_files = ["transcriber.py", "requirements.txt"]
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename} found")
        else:
            print(f"✗ {filename} missing")
            return False
    
    print("\n🎉 All tests passed!")
    return True

if __name__ == "__main__":
    success = quick_test()
    if not success:
        print("\n❌ Some tests failed. Please check your installation.")
        sys.exit(1)
    else:
        print("\nYou can now run: python transcriber.py") 