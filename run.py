#!/usr/bin/env python3
"""
🎬 AMC AI STUDIOS - AUTOMATIC LAUNCHER
This script automatically installs everything and starts the app.
Just run: python3 run.py
"""

import subprocess
import sys
import os
import time

def print_header():
    """Print welcome header."""
    print("\n" + "=" * 70)
    print("🎬 AMC AI STUDIOS - AUTOMATIC SETUP & LAUNCH")
    print("=" * 70 + "\n")

def check_python():
    """Check Python version."""
    print("Step 1/3: Checking Python version...")
    if sys.version_info < (3, 10):
        print(f"❌ ERROR: Python 3.10+ required (you have {sys.version_info.major}.{sys.version_info.minor})")
        print("   Download from: https://www.python.org/downloads/")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True

def install_deps():
    """Install dependencies automatically."""
    print("\nStep 2/3: Installing dependencies (this may take a minute)...")
    
    # Essential packages
    packages = [
        "python-dotenv",
        "pydantic",
        "flask",
        "flask-cors",
        "pytz",
        "python-dateutil"
    ]
    
    try:
        for pkg in packages:
            print(f"  Installing {pkg}...", end=" ")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-q", pkg],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅")
        
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing dependencies: {e}")
        print("   Try running manually: pip install python-dotenv pydantic flask flask-cors")
        return False

def start_app():
    """Start the application."""
    print("\nStep 3/3: Starting AMC AI Studios...")
    print("-" * 70)
    
    try:
        # Change to script directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Import main module and call main()
        sys.path.insert(0, os.getcwd())
        from main import main as run_app
        run_app()
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 TIP: Check TROUBLESHOOTING.md for solutions")
        sys.exit(1)

def main():
    """Main entry point."""
    print_header()
    
    # Step 1: Check Python
    if not check_python():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_deps():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 3: Start app
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE - LAUNCHING APPLICATION")
    print("=" * 70)
    time.sleep(1)
    
    start_app()

if __name__ == "__main__":
    main()
