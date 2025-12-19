"""Main application class for AMC AI Studios."""

import logging
from typing import Optional
import threading
import webbrowser
import time

from src.core.config import Config
from src.ui.server import UIServer
from src.pipelines.orchestrator import PipelineOrchestrator
from src.pipelines.slate_manager import StudioSlateManager
from src.theater.theater_manager import TheaterManager


class AMCStudiosApp:
    """Main application controller for AMC AI Studios."""
    
    def __init__(self, config: Config):
        """
        Initialize the AMC Studios application.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = logging.getLogger("AMCStudios.App")
        
        # Validate configuration
        if not config.validate():
            self.logger.warning(
                "No AI API keys configured. Running in limited mode. "
                "Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file."
            )
        
        # Initialize components
        self.logger.info("Initializing components...")
        
        # Pipeline orchestrator - manages all AI pipelines
        self.orchestrator = PipelineOrchestrator(config)
        
        # Studio slate manager - manages multiple concurrent projects
        self.slate_manager = StudioSlateManager(config, self.orchestrator)
        
        # Theater manager - manages virtual AMC theater
        self.theater_manager = TheaterManager(config)
        
        # UI Server - web-based interface
        self.ui_server = UIServer(config, self.orchestrator, self.theater_manager, self.slate_manager)
        
        self.logger.info("Initialization complete")
    
    def run(self):
        """Run the application."""
        self.logger.info("Starting AMC AI Studios...")
        
        # Start UI server in background thread
        server_thread = threading.Thread(
            target=self.ui_server.run,
            daemon=True
        )
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        url = f"http://{self.config.flask_host}:{self.config.flask_port}"
        
        # Print clear instructions
        print("\n" + "=" * 70)
        print("🎬 AMC AI STUDIOS - READY!")
        print("=" * 70)
        print(f"\n✅ Server running at: {url}")
        print("\n📱 TO ACCESS THE APPLICATION:")
        print(f"   1. Open your web browser")
        print(f"   2. Navigate to: {url}")
        print(f"\n⏹️  TO STOP: Press Ctrl+C")
        print("=" * 70 + "\n")
        
        try:
            webbrowser.open(url)
            self.logger.info(f"Browser opened automatically to {url}")
        except Exception as e:
            self.logger.info(f"Could not open browser automatically (this is normal in some environments)")
        
        # Keep main thread alive
        self.logger.info("Application running. Press Ctrl+C to exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.logger.info("Shutting down...")
            self.shutdown()
    
    def shutdown(self):
        """Cleanup and shutdown the application."""
        self.logger.info("Performing cleanup...")
        # Additional cleanup if needed
        self.logger.info("Shutdown complete")
