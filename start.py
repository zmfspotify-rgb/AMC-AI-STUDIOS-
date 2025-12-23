#!/usr/bin/env python3
"""
Simple launcher for AMC AI Studios that checks dependencies and starts the app.
This can be used instead of launch.bat for quick testing or on non-Windows systems.
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is sufficient."""
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies."""
    print("Checking/installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def main():
    """Main launcher function."""
    print("=" * 70)
    print("AMC AI STUDIOS - Launcher")
    print("=" * 70)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start the application
    print()
    print("Starting AMC AI Studios...")
    print()
    
    try:
        # Import and run the main application
        import main as app_main
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nShutdown requested")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
