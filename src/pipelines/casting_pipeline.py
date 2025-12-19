"""Casting pipeline for assigning AI actors to characters."""

import logging
import uuid
import json
from typing import List, Dict
from pathlib import Path

from src.core.config import Config
from src.models.schema import Project, ActorProfile, Character
from src.utils.ai_client import AIClient


class CastingPipeline:
    """AI-powered casting system."""
    
    def __init__(self, config: Config):
        """Initialize casting pipeline."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.CastingPipeline")
        self.ai_client = AIClient(config)
        
        # Load existing actors
        self.actors: Dict[str, ActorProfile] = {}
        self._load_actors()
    
    def cast_project(self, project: Project):
        """
        Assign AI actors to all characters in the project.
        
        Args:
            project: The production project
        """
        self.logger.info(f"Casting project: {project.title}")
        
        if not project.script or not project.script.characters:
            self.logger.warning("No characters to cast")
            return
        
        for character in project.script.characters:
            # Try to find existing actor or create new one
            actor = self._find_or_create_actor(character, project)
            character.assigned_actor_id = actor.id
            self.logger.info(f"Cast {actor.name} as {character.name}")
    
    def _find_or_create_actor(self, character: Character, project: Project) -> ActorProfile:
        """Find suitable actor or create a new one."""
        
        # For now, always create new actors to ensure uniqueness
        # In a real system, you'd implement similarity matching
        actor = self._create_actor(character, project)
        return actor
    
    def _create_actor(self, character: Character, project: Project) -> ActorProfile:
        """Create a new AI actor profile."""
        
        # Generate actor details using AI
        prompt = f"""
        Create a detailed AI actor profile for the following character:
        
        Character Name: {character.name}
        Description: {character.description}
        Personality: {', '.join(character.personality_traits)}
        
        Provide realistic details for:
        - actor_name (different from character name)
        - age (appropriate for the role)
        - gender
        - ethnicity
        - body_type
        - acting_style
        
        Return as JSON.
        """
        
        response = self.ai_client.generate_text(prompt, max_tokens=500)
        
        try:
            actor_data = json.loads(response)
        except:
            # Use defaults if parsing fails
            actor_data = {
                "actor_name": f"Actor {uuid.uuid4().hex[:8]}",
                "age": 30,
                "gender": "Non-binary",
                "ethnicity": "Diverse",
                "body_type": "Average",
                "acting_style": "Method"
            }
        
        actor_id = str(uuid.uuid4())
        
        actor = ActorProfile(
            id=actor_id,
            name=actor_data.get("actor_name", f"Actor {actor_id[:8]}"),
            age=actor_data.get("age", 30),
            gender=actor_data.get("gender", "Non-binary"),
            ethnicity=actor_data.get("ethnicity", "Diverse"),
            body_type=actor_data.get("body_type", "Average"),
            acting_style=actor_data.get("acting_style", "Method"),
            emotional_range=character.personality_traits,
            career_history=[f"{project.title} - {character.name}"]
        )
        
        # Save actor
        self.actors[actor_id] = actor
        self._save_actor(actor)
        
        self.logger.info(f"Created new actor: {actor.name}")
        return actor
    
    def _save_actor(self, actor: ActorProfile):
        """Save actor profile to disk."""
        actor_file = self.config.actors_dir / f"{actor.id}.json"
        
        with open(actor_file, 'w') as f:
            json.dump(actor.model_dump(mode='json'), f, indent=2, default=str)
    
    def _load_actors(self):
        """Load existing actor profiles."""
        if not self.config.actors_dir.exists():
            return
        
        for actor_file in self.config.actors_dir.glob("*.json"):
            try:
                with open(actor_file, 'r') as f:
                    actor_data = json.load(f)
                    actor = ActorProfile(**actor_data)
                    self.actors[actor.id] = actor
            except Exception as e:
                self.logger.error(f"Failed to load actor from {actor_file}: {e}")
    
    def get_actor(self, actor_id: str) -> ActorProfile:
        """Get actor by ID."""
        return self.actors.get(actor_id)
