"""Virtual AMC Theater manager."""

import logging
import random
from typing import List, Dict
import uuid

from src.core.config import Config
from src.models.schema import NPCState, Project
from src.theater.npc_ai import NPCAI


class TheaterManager:
    """Manages the virtual AMC theater experience."""
    
    def __init__(self, config: Config):
        """Initialize theater manager."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.Theater")
        
        # Theater state
        self.npcs: Dict[str, NPCState] = {}
        self.npc_ai = NPCAI(config)
        
        # Available movies (from completed projects)
        self.now_showing: List[Project] = []
        
        # Theater locations
        self.locations = {
            "lobby": {"capacity": 50, "type": "social"},
            "ticket_counter": {"capacity": 10, "type": "service"},
            "concessions": {"capacity": 15, "type": "service"},
            "hallway": {"capacity": 30, "type": "transit"},
            "theater_1": {"capacity": 100, "type": "viewing"},
            "theater_2": {"capacity": 100, "type": "viewing"},
            "theater_3": {"capacity": 75, "type": "viewing"},
        }
        
        # Initialize NPCs
        self._initialize_npcs()
        
        self.logger.info(f"Theater initialized with {len(self.npcs)} NPCs")
    
    def _initialize_npcs(self):
        """Create initial NPCs."""
        first_names = [
            "Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey",
            "Riley", "Avery", "Quinn", "Blake", "Drew", "Reese",
            "Charlie", "Jamie", "Skylar", "Cameron", "Dakota", "Emerson",
            "Harper", "Peyton"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones",
            "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"
        ]
        
        for i in range(self.config.npc_count):
            npc_id = str(uuid.uuid4())
            
            npc = NPCState(
                id=npc_id,
                name=f"{random.choice(first_names)} {random.choice(last_names)}",
                position=[random.uniform(-10, 10), 0, random.uniform(-10, 10)],
                current_action="entering_lobby",
                emotional_state=random.choice(["happy", "excited", "neutral", "relaxed"])
            )
            
            self.npcs[npc_id] = npc
    
    def update(self, delta_time: float = 1.0):
        """
        Update theater state and NPC behaviors.
        
        Args:
            delta_time: Time elapsed since last update
        """
        # Update each NPC
        for npc in self.npcs.values():
            self.npc_ai.update_npc(npc, self.locations, delta_time)
    
    def add_movie_to_theater(self, project: Project):
        """
        Add a completed movie to the now showing list.
        
        Args:
            project: Completed project to show
        """
        if project.final_video_path:
            self.now_showing.append(project)
            self.logger.info(f"Added to now showing: {project.title}")
    
    def get_theater_state(self) -> Dict:
        """Get current state of the theater."""
        return {
            "npcs": [npc.model_dump() for npc in self.npcs.values()],
            "now_showing": [
                {
                    "id": p.id,
                    "title": p.title,
                    "rating": p.rating,
                    "genres": p.genres,
                    "runtime": p.runtime_minutes
                }
                for p in self.now_showing
            ],
            "locations": self.locations
        }
    
    def get_npc_at_location(self, location: str) -> List[NPCState]:
        """Get all NPCs at a specific location."""
        return [
            npc for npc in self.npcs.values()
            if npc.target_location == location or location in npc.current_action
        ]
