"""NPC AI behavior system."""

import logging
import random
from typing import Dict, List

from src.core.config import Config
from src.models.schema import NPCState


class NPCAI:
    """AI system for NPC behaviors in the theater."""
    
    def __init__(self, config: Config):
        """Initialize NPC AI."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.NPCAI")
        
        # Behavior weights
        self.behavior_weights = {
            "buy_ticket": 0.3,
            "buy_concessions": 0.25,
            "watch_movie": 0.3,
            "socialize": 0.1,
            "leave": 0.05
        }
    
    def update_npc(self, npc: NPCState, locations: Dict, delta_time: float):
        """
        Update a single NPC's behavior.
        
        Args:
            npc: The NPC to update
            locations: Available theater locations
            delta_time: Time elapsed
        """
        # State machine for NPC behavior
        if npc.current_action == "entering_lobby":
            self._handle_entering_lobby(npc)
        
        elif npc.current_action == "idle":
            self._decide_next_action(npc)
        
        elif npc.current_action == "walking_to_ticket_counter":
            if self._reached_destination(npc, "ticket_counter"):
                npc.current_action = "buying_ticket"
        
        elif npc.current_action == "buying_ticket":
            if random.random() < 0.3:  # 30% chance per update to finish
                npc.has_ticket = True
                npc.current_action = "idle"
                npc.emotional_state = "happy"
        
        elif npc.current_action == "walking_to_concessions":
            if self._reached_destination(npc, "concessions"):
                npc.current_action = "buying_concessions"
        
        elif npc.current_action == "buying_concessions":
            if random.random() < 0.25:  # 25% chance per update to finish
                npc.has_concessions = True
                npc.current_action = "idle"
        
        elif npc.current_action == "walking_to_theater":
            if self._reached_destination(npc, npc.target_location):
                npc.current_action = "entering_theater"
        
        elif npc.current_action == "entering_theater":
            npc.current_action = "finding_seat"
        
        elif npc.current_action == "finding_seat":
            npc.current_action = "sitting"
            npc.emotional_state = "excited"
        
        elif npc.current_action == "sitting":
            if random.random() < 0.1:  # Randomly start watching
                npc.current_action = "watching_movie"
        
        elif npc.current_action == "watching_movie":
            # React to movie
            self._react_to_movie(npc)
            
            # Small chance to finish watching
            if random.random() < 0.02:
                npc.current_action = "leaving_theater"
                npc.emotional_state = "satisfied"
        
        elif npc.current_action == "leaving_theater":
            npc.current_action = "walking_to_exit"
        
        elif npc.current_action == "walking_to_exit":
            if random.random() < 0.2:
                # Leave the theater completely
                npc.current_action = "exited"
        
        elif npc.current_action == "socializing":
            if random.random() < 0.15:
                npc.current_action = "idle"
        
        # Update position (simple movement simulation)
        self._update_position(npc, delta_time)
    
    def _handle_entering_lobby(self, npc: NPCState):
        """Handle NPC entering the lobby."""
        if random.random() < 0.5:
            npc.current_action = "idle"
            npc.target_location = "lobby"
    
    def _decide_next_action(self, npc: NPCState):
        """Decide what the NPC should do next."""
        
        # If no ticket, prioritize getting one
        if not npc.has_ticket:
            if random.random() < 0.7:
                npc.current_action = "walking_to_ticket_counter"
                npc.target_location = "ticket_counter"
                return
        
        # If has ticket but no concessions, maybe get some
        if npc.has_ticket and not npc.has_concessions:
            if random.random() < 0.6:
                npc.current_action = "walking_to_concessions"
                npc.target_location = "concessions"
                return
        
        # If has ticket, go watch movie
        if npc.has_ticket:
            if random.random() < 0.5:
                theater = random.choice(["theater_1", "theater_2", "theater_3"])
                npc.current_action = "walking_to_theater"
                npc.target_location = theater
                return
        
        # Otherwise, socialize or idle
        if random.random() < 0.3:
            npc.current_action = "socializing"
        # Else stay idle
    
    def _reached_destination(self, npc: NPCState, location: str) -> bool:
        """Check if NPC reached their destination."""
        # Simplified: random chance based on "walking time"
        return random.random() < 0.2
    
    def _react_to_movie(self, npc: NPCState):
        """Make NPC react to the movie they're watching."""
        reactions = [
            ("laugh", "amused"),
            ("gasp", "surprised"),
            ("clap", "excited"),
            ("cry", "emotional"),
            ("cheer", "happy"),
            (None, "focused")  # Just watching
        ]
        
        if random.random() < 0.1:  # 10% chance to react each update
            reaction, emotion = random.choice(reactions)
            if reaction:
                self.logger.debug(f"{npc.name} reacts: {reaction}")
            npc.emotional_state = emotion
    
    def _update_position(self, npc: NPCState, delta_time: float):
        """Update NPC physical position."""
        # Simple random walk when moving
        if "walking" in npc.current_action:
            npc.position[0] += random.uniform(-0.1, 0.1) * delta_time
            npc.position[2] += random.uniform(-0.1, 0.1) * delta_time
            
            # Keep in bounds
            npc.position[0] = max(-20, min(20, npc.position[0]))
            npc.position[2] = max(-20, min(20, npc.position[2]))
