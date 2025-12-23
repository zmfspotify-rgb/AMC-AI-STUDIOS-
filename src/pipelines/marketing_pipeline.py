"""Marketing pipeline for creating promotional materials."""

import logging
from pathlib import Path
import json

from src.core.config import Config
from src.models.schema import Project
from src.utils.ai_client import AIClient


class MarketingPipeline:
    """AI-powered marketing and promotional content generation."""
    
    def __init__(self, config: Config):
        """Initialize marketing pipeline."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.Marketing")
        self.ai_client = AIClient(config)
    
    def create_marketing_materials(self, project: Project):
        """
        Generate all marketing materials for the project.
        
        Args:
            project: The production project
        """
        self.logger.info(f"Creating marketing materials for: {project.title}")
        
        # Create marketing directory
        marketing_dir = self.config.assets_dir / project.id / "marketing"
        marketing_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate poster
        poster_path = self._generate_poster(project, marketing_dir)
        project.poster_path = poster_path
        
        # Generate trailers
        trailer_path = self._generate_trailers(project, marketing_dir)
        project.trailer_path = trailer_path
        
        # Generate social media assets
        self._generate_social_media_assets(project, marketing_dir)
        
        # Create press release
        self._create_press_release(project, marketing_dir)
        
        self.logger.info("Marketing materials created")
    
    def _generate_poster(self, project: Project, marketing_dir: Path) -> str:
        """Generate movie poster."""
        self.logger.info("Generating poster...")
        
        # Create poster description for image generation
        poster_prompt = f"""
        Create a cinematic movie poster for:
        
        Title: {project.title}
        Genre: {', '.join(project.genres)}
        Rating: {project.rating}
        Logline: {project.script.logline if project.script else project.story_summary}
        
        Style: {self._get_poster_style(project)}
        """
        
        # In real implementation, generate image using DALL-E or Stable Diffusion
        # For now, save metadata
        poster_metadata = {
            "title": project.title,
            "prompt": poster_prompt,
            "style": self._get_poster_style(project),
            "dimensions": "27x40 inches (movie poster standard)"
        }
        
        poster_file = marketing_dir / "poster_metadata.json"
        with open(poster_file, 'w') as f:
            json.dump(poster_metadata, f, indent=2)
        
        return str(poster_file)
    
    def _generate_trailers(self, project: Project, marketing_dir: Path) -> str:
        """Generate movie trailers."""
        self.logger.info("Generating trailers...")
        
        # Create different trailer versions
        trailer_types = [
            "Teaser (30s)",
            "Trailer 1 (1:30)",
            "Trailer 2 (2:00)",
            "Final Trailer (2:30)"
        ]
        
        trailers_metadata = {
            "trailers": []
        }
        
        for trailer_type in trailer_types:
            # In real implementation:
            # 1. Select key scenes
            # 2. Add dramatic music
            # 3. Add title cards
            # 4. Create suspenseful edit
            
            trailer_info = {
                "type": trailer_type,
                "description": self._create_trailer_description(project, trailer_type)
            }
            trailers_metadata["trailers"].append(trailer_info)
        
        trailers_file = marketing_dir / "trailers_metadata.json"
        with open(trailers_file, 'w') as f:
            json.dump(trailers_metadata, f, indent=2)
        
        return str(trailers_file)
    
    def _generate_social_media_assets(self, project: Project, marketing_dir: Path):
        """Generate social media promotional content."""
        self.logger.info("Generating social media assets...")
        
        social_assets = {
            "posts": [],
            "clips": [],
            "graphics": []
        }
        
        # Create announcement posts
        social_assets["posts"].append({
            "platform": "Twitter/X",
            "content": f"🎬 Coming Soon: {project.title}\n{project.script.logline if project.script else project.story_summary}\n#{project.title.replace(' ', '')}"
        })
        
        social_assets["posts"].append({
            "platform": "Instagram",
            "content": f"🎥 {project.title}\nA {', '.join(project.genres)} {project.project_type.value}\nComing to AMC Theaters\n#{project.title.replace(' ', '')} #AMC #Movies"
        })
        
        # Create countdown graphics
        for days in [30, 14, 7, 3, 1]:
            social_assets["graphics"].append({
                "type": "countdown",
                "days_until_release": days,
                "text": f"{days} DAYS UNTIL {project.title.upper()}"
            })
        
        social_file = marketing_dir / "social_media.json"
        with open(social_file, 'w') as f:
            json.dump(social_assets, f, indent=2)
    
    def _create_press_release(self, project: Project, marketing_dir: Path):
        """Create press release."""
        self.logger.info("Creating press release...")
        
        press_release = f"""
        FOR IMMEDIATE RELEASE
        
        AMC AI STUDIOS ANNOUNCES: {project.title.upper()}
        
        {project.script.logline if project.script else project.story_summary}
        
        AMC AI Studios is proud to announce the upcoming release of {project.title}, 
        a {', '.join(project.genres)} {project.project_type.value} rated {project.rating}.
        
        This groundbreaking production represents the future of entertainment, 
        created entirely through advanced AI technology while maintaining the heart 
        and soul of great storytelling.
        
        Coming soon to AMC Virtual Theaters.
        
        About AMC AI Studios:
        AMC AI Studios is revolutionizing entertainment production through the power 
        of artificial intelligence, creating compelling stories brought to life by 
        cutting-edge technology.
        
        ###
        """
        
        press_file = marketing_dir / "press_release.txt"
        with open(press_file, 'w') as f:
            f.write(press_release)
    
    def _get_poster_style(self, project: Project) -> str:
        """Determine poster art style based on genre."""
        if "Horror" in project.genres:
            return "dark, ominous, dramatic lighting"
        elif "Romance" in project.genres:
            return "warm, intimate, soft focus"
        elif "Action" in project.genres:
            return "dynamic, explosive, high contrast"
        elif "Sci-Fi" in project.genres:
            return "futuristic, sleek, cosmic"
        else:
            return "cinematic, professional, eye-catching"
    
    def _create_trailer_description(self, project: Project, trailer_type: str) -> str:
        """Create description for trailer generation."""
        return f"{trailer_type} showcasing key moments from {project.title}"
