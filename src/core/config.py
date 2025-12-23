"""Core configuration management for AMC AI Studios."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration manager."""
    
    def __init__(self):
        """Initialize configuration from environment."""
        # Load environment variables
        load_dotenv()
        
        # Base paths
        self.base_dir = Path(__file__).parent.parent.parent
        self.data_dir = self.base_dir / "data"
        
        # Application settings
        self.app_name = os.getenv("APP_NAME", "AMC AI Studios")
        self.app_version = os.getenv("APP_VERSION", "1.0.0")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        
        # Directory paths
        self.projects_dir = self.data_dir / "projects"
        self.assets_dir = self.data_dir / "assets"
        self.actors_dir = self.data_dir / "actors"
        self.cache_dir = self.data_dir / "cache"
        
        # Database
        self.database_url = os.getenv("DATABASE_URL", f"sqlite:///{self.data_dir}/amc_studios.db")
        
        # AI Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.default_llm_model = os.getenv("DEFAULT_LLM_MODEL", "gpt-4-turbo-preview")
        self.default_image_model = os.getenv("DEFAULT_IMAGE_MODEL", "dall-e-3")
        
        # Processing settings
        self.max_concurrent_jobs = int(os.getenv("MAX_CONCURRENT_JOBS", "3"))
        self.gpu_enabled = os.getenv("GPU_ENABLED", "True").lower() == "true"
        self.offline_mode = os.getenv("OFFLINE_MODE", "False").lower() == "true"
        
        # Theater settings
        self.theater_capacity = int(os.getenv("THEATER_CAPACITY", "100"))
        self.npc_count = int(os.getenv("NPC_COUNT", "20"))
        
        # Server settings
        self.flask_host = os.getenv("FLASK_HOST", "127.0.0.1")
        self.flask_port = int(os.getenv("FLASK_PORT", "5000"))
        self.flask_debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.data_dir,
            self.projects_dir,
            self.assets_dir,
            self.actors_dir,
            self.cache_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> bool:
        """Validate configuration."""
        if not self.offline_mode:
            if not self.openai_api_key and not self.anthropic_api_key:
                return False
        return True
