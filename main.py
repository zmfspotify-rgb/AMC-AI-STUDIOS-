"""
AMC AI Studios - Main Entry Point
A fully functional AI-powered movie and television studio with virtual AMC theater.
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Check and install dependencies if needed
def check_dependencies():
    """Check if required dependencies are installed, install if missing."""
    required = {
        'dotenv': 'python-dotenv',
        'pydantic': 'pydantic',
        'flask': 'flask',
        'flask_cors': 'flask-cors'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("=" * 70)
        print("🔧 MISSING DEPENDENCIES DETECTED")
        print("=" * 70)
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\nInstalling dependencies automatically...")
        print()
        
        import subprocess
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-q"
            ] + missing)
            print("✅ Dependencies installed successfully!")
            print("\n⚠️  Restarting to load new dependencies...")
            print()
            
            # Restart the script
            os.execv(sys.executable, [sys.executable] + sys.argv)
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Failed to install dependencies: {e}")
            print("\nPlease install manually:")
            print(f"  pip install {' '.join(missing)}")
            print("\nOr use the automatic launcher:")
            print("  Windows: RUN.bat")
            print("  Mac/Linux: python3 run.py")
            print()
            return False
    return True

# Install dependencies if needed
if not check_dependencies():
    sys.exit(1)

from src.core.config import Config
from src.core.app import AMCStudiosApp
from src.utils.logger import setup_logger


def main():
    """Main entry point for AMC AI Studios."""
    
    # Setup logging
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("AMC AI STUDIOS - Starting...")
    logger.info("=" * 60)
    
    try:
        # Initialize configuration
        config = Config()
        config.ensure_directories()
        
        # Create and run the application
        app = AMCStudiosApp(config)
        app.run()
        
    except KeyboardInterrupt:
        logger.info("\nShutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
