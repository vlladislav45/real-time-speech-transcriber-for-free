#!/usr/bin/env python3
"""
Installation Script for Speech Transcriber
This script helps install dependencies and set up the environment
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        import pip
        print("✓ pip is available")
        return True
    except ImportError:
        print("❌ pip is not available")
        return False

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def install_requirements():
    """Install requirements from requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def install_pyaudio():
    """Install PyAudio with platform-specific handling"""
    print("Installing PyAudio...")
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("Detected macOS")
        try:
            # Try to install portaudio first
            subprocess.run(["brew", "install", "portaudio"], check=True)
            print("✓ PortAudio installed via Homebrew")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠ Homebrew not found or portaudio installation failed")
            print("You may need to install Homebrew: https://brew.sh/")
        
        # Try to install pyaudio
        if install_package("pyaudio"):
            print("✓ PyAudio installed")
            return True
        else:
            print("❌ PyAudio installation failed")
            print("Try: pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio")
            return False
    
    elif system == "Windows":
        print("Detected Windows")
        if install_package("pyaudio"):
            print("✓ PyAudio installed")
            return True
        else:
            print("❌ PyAudio installation failed")
            print("Try: pip install pipwin && pipwin install pyaudio")
            return False
    
    elif system == "Linux":
        print("Detected Linux")
        print("You may need to install system dependencies first:")
        print("sudo apt-get install python3-pyaudio portaudio19-dev")
        if install_package("pyaudio"):
            print("✓ PyAudio installed")
            return True
        else:
            print("❌ PyAudio installation failed")
            return False
    
    else:
        print(f"Unknown system: {system}")
        if install_package("pyaudio"):
            print("✓ PyAudio installed")
            return True
        else:
            print("❌ PyAudio installation failed")
            return False

def create_virtual_environment():
    """Create a virtual environment"""
    if os.path.exists("venv"):
        print("✓ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✓ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def setup_environment():
    """Set up the complete environment"""
    print("=== Speech Transcriber Installation ===")
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    if not check_pip():
        return False
    
    # Ask user preference
    print("\nInstallation options:")
    print("1. Create virtual environment (recommended)")
    print("2. Install globally")
    print("3. Exit")
    
    while True:
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == "1":
            # Virtual environment setup
            if not create_virtual_environment():
                return False
            
            # Activate virtual environment and install packages
            if platform.system() == "Windows":
                activate_script = os.path.join("venv", "Scripts", "activate")
                pip_path = os.path.join("venv", "Scripts", "pip")
            else:
                activate_script = os.path.join("venv", "bin", "activate")
                pip_path = os.path.join("venv", "bin", "pip")
            
            print("Installing packages in virtual environment...")
            
            # Install basic packages
            if not subprocess.call([pip_path, "install", "SpeechRecognition"]):
                print("✓ SpeechRecognition installed")
            else:
                print("❌ SpeechRecognition installation failed")
                return False
            
            # Install PyAudio
            if install_pyaudio():
                print("✓ PyAudio installed")
            else:
                print("❌ PyAudio installation failed")
                return False
            
            print("\n🎉 Installation complete!")
            print("\nTo use the application:")
            print("1. Activate virtual environment:")
            if platform.system() == "Windows":
                print("   venv\\Scripts\\activate")
            else:
                print("   source venv/bin/activate")
            print("2. Run the application:")
            print("   python transcriber.py")
            print("   python transcriber_improved.py")
            print("   python transcriber_fast.py")
            print("   python transcriber_realtime.py")
            print("   python log_viewer.py")
            print("   ./run.sh")
            break
            
        elif choice == "2":
            # Global installation
            print("Installing packages globally...")
            
            if not install_package("SpeechRecognition"):
                print("❌ SpeechRecognition installation failed")
                return False
            
            if not install_pyaudio():
                print("❌ PyAudio installation failed")
                return False
            
            print("\n🎉 Installation complete!")
            print("\nYou can now run:")
            print("  python transcriber.py")
            print("  python transcriber_improved.py")
            print("  python transcriber_fast.py")
            print("  python transcriber_realtime.py")
            print("  python log_viewer.py")
            print("  ./run.sh")
            break
            
        elif choice == "3":
            print("Installation cancelled.")
            return False
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    return True

def main():
    """Main installation function"""
    try:
        success = setup_environment()
        if success:
            print("\n✅ Installation successful!")
            print("Run 'python test_installation.py' to verify the installation.")
        else:
            print("\n❌ Installation failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 