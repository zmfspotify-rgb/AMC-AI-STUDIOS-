"""Virtual AMC Theater manager."""

import logging
import random
from typing import List, Dict
import uuid

from src.core.config import Config
from src.models.schema import NPCState, Project
from src.theater.npc_ai import NPCAI
from src.theater.ticketing import TicketingSystem
from src.theater.release_manager import ReleaseManager
from src.theater.npc_intelligence import NPCAudienceIntelligence


class TheaterManager:
    """Manages the virtual AMC theater experience."""
    
    def __init__(self, config: Config):
        """Initialize theater manager."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.Theater")
        
        # Initialize subsystems
        self.ticketing = TicketingSystem(config)
        self.release_manager = ReleaseManager(config)
        self.npc_intelligence = NPCAudienceIntelligence(config)
        
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
            "red_carpet": {"capacity": 200, "type": "event"},
            "press_room": {"capacity": 50, "type": "viewing"},
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
            # Check if released
            if self.release_manager.check_release_unlock(project):
                self.now_showing.append(project)
                
                # Generate showtimes for the week
                self.ticketing.generate_showtimes_for_week(project)
                
                self.logger.info(f"Added to now showing: {project.title}")
            else:
                self.logger.info(f"{project.title} not yet released")
    
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
                    "runtime": p.runtime_minutes,
                    "average_rating": p.average_rating,
                    "box_office": p.box_office_total,
                    "release_status": self.release_manager.get_release_status(p)
                }
                for p in self.now_showing
            ],
            "locations": self.locations,
            "active_red_carpet": self._get_active_red_carpet_events()
        }
    
    def get_npc_at_location(self, location: str) -> List[NPCState]:
        """Get all NPCs at a specific location."""
        return [
            npc for npc in self.npcs.values()
            if npc.target_location == location or location in npc.current_action
        ]
    
    def _get_active_red_carpet_events(self) -> List[Dict]:
        """Get active red carpet events."""
        active_events = []
        for project in self.now_showing:
            event = self.release_manager.check_red_carpet_active(project.id)
            if event:
                active_events.append({
                    "project_id": project.id,
                    "project_title": project.title,
                    "event_id": event.event_id,
                    "is_active": event.is_active
                })
        return active_events
    
    def purchase_ticket_for_npc(self, npc: NPCState, project: Project):
        """
        NPC purchases a ticket.
        
        Args:
            npc: NPC purchasing
            project: Project to watch
        """
        # Get available showtimes
        if project.id in self.ticketing.showtimes:
            showtimes = self.ticketing.showtimes[project.id]
            if showtimes:
                showtime = random.choice(showtimes)
                
                # Get available seats
                theater_id = showtime.theater_id
                available_seats = self.ticketing.get_available_seats(theater_id)
                
                if available_seats:
                    seat = random.choice(available_seats)
                    
                    ticket = self.ticketing.purchase_ticket(
                        project.id,
                        theater_id,
                        seat.seat_id,
                        showtime,
                        npc.id
                    )
                    
                    if ticket:
                        npc.has_ticket = True
                        npc.ticket_id = ticket.ticket_id
                        npc.seat_number = seat.seat_id
                        self.logger.info(f"{npc.name} purchased ticket for {project.title}")
    
    def simulate_npc_watching_movie(self, npc: NPCState, project: Project):
        """
        Simulate NPC watching a movie and generate review.
        
        Args:
            npc: NPC watching
            project: Project being watched
        """
        # Generate emotional reactions
        reactions = []
        num_reactions = random.randint(3, 8)
        
        possible_reactions = [
            "laugh", "gasp_positive", "gasp_negative", 
            "clap", "cheer", "surprised", "emotional"
        ]
        
        for _ in range(num_reactions):
            reactions.append(random.choice(possible_reactions))
        
        # Generate review
        review = self.npc_intelligence.generate_npc_review(npc, project, reactions)
        
        # Update box office
        self.npc_intelligence.track_box_office(project, 1)
        
        npc.movie_watching = project.id
        
        return review
