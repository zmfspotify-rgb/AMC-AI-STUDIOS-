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
