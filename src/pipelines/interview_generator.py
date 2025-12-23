"""AI interview and press content generation system."""

import logging
import uuid
import random
from pathlib import Path
import json

from src.core.config import Config
from src.models.schema import Project, Interview, ActorProfile
from src.utils.ai_client import AIClient


class InterviewGenerator:
    """Generates AI interviews and press content."""
    
    def __init__(self, config: Config):
        """Initialize interview generator."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.Interviews")
        self.ai_client = AIClient(config)
        
        # Interviewer personalities
        self.interviewers = {
            "serious": {
                "name": "James Chronicle",
                "style": "In-depth, analytical, industry-focused"
            },
            "funny": {
                "name": "Alexa Bright",
                "style": "Witty, energetic, audience-pleasing"
            },
            "chaotic": {
                "name": "Max Wilde",
                "style": "Unpredictable, edgy, viral moments"
            },
            "fan_focused": {
                "name": "Taylor Fansworth",
                "style": "Enthusiastic, relatable, fan questions"
            }
        }
    
    def generate_interview(
        self,
        project: Project,
        actors: list,
        interview_type: str = "sit-down",
        personality: str = "serious"
    ) -> Interview:
        """
        Generate an AI interview.
        
        Args:
            project: The project being promoted
            actors: List of ActorProfile objects
            interview_type: Type of interview
            personality: Interviewer personality
            
        Returns:
            Generated interview
        """
        self.logger.info(f"Generating {interview_type} interview for {project.title}")
        
        interviewer = self.interviewers[personality]
        
        # Generate interview content
        content = self._generate_interview_content(
            project, actors, interview_type, interviewer
        )
        
        # Create interview directory
        interview_dir = self.config.assets_dir / project.id / "interviews"
        interview_dir.mkdir(parents=True, exist_ok=True)
        
        interview_id = str(uuid.uuid4())
        content_file = interview_dir / f"interview_{interview_id}.json"
        
        with open(content_file, 'w') as f:
            json.dump(content, f, indent=2)
        
        interview = Interview(
            interview_id=interview_id,
            project_id=project.id,
            title=content["title"],
            interviewer_name=interviewer["name"],
            interviewer_personality=personality,
            actors=[actor.id for actor in actors],
            content_path=str(content_file),
            interview_type=interview_type,
            duration=content["duration"]
        )
        
        self.logger.info(f"Interview generated: {interview.title}")
        return interview
    
    def _generate_interview_content(
        self,
        project: Project,
        actors: list,
        interview_type: str,
        interviewer: dict
    ) -> dict:
        """Generate the actual interview content."""
        
        actor_names = [actor.name for actor in actors]
        
        content = {
            "title": f"{interviewer['name']} sits down with the cast of {project.title}",
            "interviewer": interviewer["name"],
            "style": interviewer["style"],
            "guests": actor_names,
            "duration": random.randint(480, 1800),  # 8-30 minutes
            "segments": []
        }
        
        if interview_type == "sit-down":
            content["segments"] = self._create_sitdown_segments(project, actors, interviewer)
        elif interview_type == "late-night":
            content["segments"] = self._create_latenight_segments(project, actors)
        elif interview_type == "game":
            content["segments"] = self._create_game_segments(project, actors)
        elif interview_type == "roundtable":
            content["segments"] = self._create_roundtable_segments(project, actors)
        elif interview_type == "behind-the-scenes":
            content["segments"] = self._create_bts_segments(project, actors)
        
        return content
    
    def _create_sitdown_segments(self, project, actors, interviewer):
        """Create sit-down interview segments."""
        segments = [
            {
                "segment": "Opening",
                "topic": f"Welcome and introduction to {project.title}",
                "questions": [
                    f"Tell us about {project.title}",
                    "What drew you to this project?",
                    "How would you describe this story?"
                ]
            },
            {
                "segment": "Character Discussion",
                "topic": "Deep dive into characters",
                "questions": [
                    "Tell us about your character",
                    "What was your preparation process?",
                    "Any memorable moments from filming?"
                ]
            },
            {
                "segment": "Behind the Scenes",
                "topic": "Production stories",
                "questions": [
                    "What was the atmosphere on set?",
                    "Any funny moments during production?",
                    "What surprised you most about this project?"
                ]
            },
            {
                "segment": "Final Thoughts",
                "topic": "Closing remarks",
                "questions": [
                    "What do you want audiences to take away?",
                    "Any teases for what's next?"
                ]
            }
        ]
        return segments
    
    def _create_latenight_segments(self, project, actors):
        """Create late-night show segments."""
        return [
            {"segment": "Monologue Entrance", "duration": 60},
            {"segment": "Fun Anecdote", "duration": 180},
            {"segment": "Movie Clip", "duration": 120},
            {"segment": "Quick Game", "duration": 240},
            {"segment": "Closing Plug", "duration": 60}
        ]
    
    def _create_game_segments(self, project, actors):
        """Create game-style interview segments."""
        games = [
            "Two Truths and a Lie about the Movie",
            "Act Out Your Scene with Props",
            "Guess the Co-Star's Quote",
            "Rapid Fire Questions",
            "Charades: Movie Edition"
        ]
        
        return [
            {"segment": "Introduction", "duration": 60},
            {"segment": "Game 1", "game": random.choice(games), "duration": 300},
            {"segment": "Game 2", "game": random.choice(games), "duration": 300},
            {"segment": "Lightning Round", "duration": 120}
        ]
    
    def _create_roundtable_segments(self, project, actors):
        """Create roundtable discussion segments."""
        return [
            {
                "segment": "Opening Discussion",
                "topic": "The Vision",
                "duration": 300
            },
            {
                "segment": "Character Dynamics",
                "topic": "Relationships and Chemistry",
                "duration": 600
            },
            {
                "segment": "Themes and Messages",
                "topic": "Deeper Meaning",
                "duration": 480
            },
            {
                "segment": "Audience Q&A",
                "topic": "Fan Questions",
                "duration": 420
            }
        ]
    
    def _create_bts_segments(self, project, actors):
        """Create behind-the-scenes segments."""
        return [
            {"segment": "Introduction", "duration": 60},
            {"segment": "Set Tour", "duration": 300},
            {"segment": "Costume and Makeup", "duration": 240},
            {"segment": "Special Effects Breakdown", "duration": 360},
            {"segment": "Director's Commentary", "duration": 300},
            {"segment": "Blooper Reel", "duration": 180}
        ]
    
    def generate_press_tour(self, project: Project, actors: list) -> list:
        """
        Generate a complete press tour with multiple interviews.
        
        Args:
            project: Project being promoted
            actors: List of actors
            
        Returns:
            List of Interview objects
        """
        self.logger.info(f"Generating press tour for {project.title}")
        
        interviews = []
        
        # Variety of interview types
        interview_schedule = [
            ("sit-down", "serious"),
            ("late-night", "funny"),
            ("game", "chaotic"),
            ("roundtable", "fan_focused"),
            ("behind-the-scenes", "serious")
        ]
        
        for interview_type, personality in interview_schedule:
            interview = self.generate_interview(
                project,
                actors,
                interview_type,
                personality
            )
            interviews.append(interview)
        
        self.logger.info(f"Press tour complete: {len(interviews)} interviews")
        return interviews
