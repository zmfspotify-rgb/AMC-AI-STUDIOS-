"""Script generation pipeline using AI."""

import logging
from typing import List, Dict, Optional
import json

from src.core.config import Config
from src.models.schema import Project, Script, Scene, Character, SceneMetadata
from src.utils.ai_client import AIClient


class ScriptPipeline:
    """AI-powered script generation pipeline."""
    
    def __init__(self, config: Config):
        """Initialize script pipeline."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.ScriptPipeline")
        self.ai_client = AIClient(config)
    
    def generate_script(self, project: Project) -> Script:
        """
        Generate a complete screenplay for the project.
        
        Args:
            project: The production project
            
        Returns:
            Generated script
        """
        self.logger.info(f"Generating script for: {project.title}")
        
        # Step 1: Generate characters
        characters = self._generate_characters(project)
        
        # Step 2: Generate scene breakdown
        num_scenes = self._calculate_num_scenes(project)
        scenes = self._generate_scenes(project, characters, num_scenes)
        
        # Create script
        script = Script(
            title=project.title,
            version="Draft 1",
            logline=self._generate_logline(project),
            characters=characters,
            scenes=scenes
        )
        
        self.logger.info(f"Script generated with {len(scenes)} scenes")
        return script
    
    def _generate_characters(self, project: Project) -> List[Character]:
        """Generate main characters for the story."""
        self.logger.info("Generating characters...")
        
        prompt = f"""
        Generate 3-5 main characters for a {project.project_type.value} with the following details:
        
        Title: {project.title}
        Genre: {', '.join(project.genres)}
        Rating: {project.rating}
        Story: {project.story_summary}
        Tone: {project.tone}
        
        For each character, provide:
        - name
        - description (2-3 sentences)
        - role (protagonist, antagonist, supporting, mentor, etc.)
        - personality_traits (list of 3-5 traits)
        - emotional_arc (brief description)
        
        Return as JSON array.
        """
        
        response = self.ai_client.generate_text(prompt, max_tokens=2000)
        
        try:
            # Parse JSON response
            characters_data = json.loads(response)
            characters = [Character(**char) for char in characters_data]
            return characters
        except Exception as e:
            self.logger.warning(f"Failed to parse characters, using defaults: {e}")
            # Create default characters
            return [
                Character(
                    name="Alex",
                    description="The protagonist",
                    role="protagonist",
                    personality_traits=["brave", "determined", "caring"]
                ),
                Character(
                    name="Morgan",
                    description="The supporting character",
                    role="supporting",
                    personality_traits=["loyal", "witty", "resourceful"]
                )
            ]
    
    def _calculate_num_scenes(self, project: Project) -> int:
        """Calculate approximate number of scenes needed."""
        if project.runtime_minutes:
            # Roughly 2-3 minutes per scene
            return max(10, project.runtime_minutes // 2)
        elif project.num_episodes:
            # TV episode typically 20-30 scenes
            return 25
        return 30
    
    def _generate_scenes(
        self,
        project: Project,
        characters: List[Character],
        num_scenes: int
    ) -> List[Scene]:
        """Generate screenplay scenes."""
        self.logger.info(f"Generating {num_scenes} scenes...")
        
        scenes = []
        character_names = [c.name for c in characters]
        
        # Generate scene outlines
        prompt = f"""
        Create a scene-by-scene outline for a {project.project_type.value}:
        
        Title: {project.title}
        Genre: {', '.join(project.genres)}
        Story: {project.story_summary}
        Characters: {', '.join(character_names)}
        Number of scenes: {num_scenes}
        
        For each scene (numbered 1-{num_scenes}), provide:
        - scene_type: "INT." or "EXT."
        - location: brief location name
        - time: "DAY", "NIGHT", "MORNING", etc.
        - action: 2-3 sentence description of what happens
        - dialogue: array of {{"character": "name", "line": "text"}} (2-4 exchanges per scene)
        
        Return as JSON array.
        """
        
        response = self.ai_client.generate_text(prompt, max_tokens=4000)
        
        try:
            scenes_data = json.loads(response)
            
            for i, scene_data in enumerate(scenes_data[:num_scenes], 1):
                # Add metadata
                metadata = SceneMetadata(
                    scene_number=i,
                    location=scene_data.get("location", "Unknown"),
                    time_of_day=scene_data.get("time", "DAY"),
                    characters=self._extract_scene_characters(scene_data.get("dialogue", [])),
                    camera_style="cinematic",
                    lighting_mood=self._determine_lighting(scene_data.get("time", "DAY"))
                )
                
                scene = Scene(
                    scene_number=i,
                    scene_type=scene_data.get("scene_type", "INT."),
                    location=scene_data.get("location", "Unknown"),
                    time=scene_data.get("time", "DAY"),
                    action=scene_data.get("action", ""),
                    dialogue=scene_data.get("dialogue", []),
                    metadata=metadata
                )
                scenes.append(scene)
                
        except Exception as e:
            self.logger.warning(f"Failed to parse scenes, using template: {e}")
            # Create template scenes
            for i in range(1, min(num_scenes, 5) + 1):
                scenes.append(self._create_template_scene(i, character_names))
        
        return scenes
    
    def _generate_logline(self, project: Project) -> str:
        """Generate a logline for the project."""
        prompt = f"""
        Create a compelling one-sentence logline for:
        
        Title: {project.title}
        Genre: {', '.join(project.genres)}
        Story: {project.story_summary}
        
        Return only the logline, no additional text.
        """
        
        logline = self.ai_client.generate_text(prompt, max_tokens=100)
        return logline.strip()
    
    def _extract_scene_characters(self, dialogue: List[Dict[str, str]]) -> List[str]:
        """Extract unique character names from dialogue."""
        characters = set()
        for line in dialogue:
            if "character" in line:
                characters.add(line["character"])
        return list(characters)
    
    def _determine_lighting(self, time: str) -> str:
        """Determine lighting mood based on time of day."""
        time_lower = time.lower()
        if "night" in time_lower:
            return "dark"
        elif "morning" in time_lower or "dawn" in time_lower:
            return "soft"
        elif "dusk" in time_lower or "evening" in time_lower:
            return "golden"
        return "bright"
    
    def _create_template_scene(self, scene_num: int, character_names: List[str]) -> Scene:
        """Create a template scene as fallback."""
        return Scene(
            scene_number=scene_num,
            scene_type="INT." if scene_num % 2 == 0 else "EXT.",
            location=f"Location {scene_num}",
            time="DAY",
            action=f"Scene {scene_num} action description.",
            dialogue=[
                {"character": character_names[0] if character_names else "Character", "line": "Dialogue line."}
            ]
        )
