"""Ticketing system for AMC AI Studios virtual theater."""

import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random

from src.core.config import Config
from src.models.schema import (
    Seat, Ticket, Showtime, Project
)


class TicketingSystem:
    """Manages ticket purchasing and seat selection."""
    
    def __init__(self, config: Config):
        """Initialize ticketing system."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.Ticketing")
        
        # Theater configurations
        self.theaters = {
            "theater_1": {"rows": 10, "seats_per_row": 10, "name": "IMAX Theater 1"},
            "theater_2": {"rows": 10, "seats_per_row": 10, "name": "Premium Theater 2"},
            "theater_3": {"rows": 8, "seats_per_row": 9, "name": "Classic Theater 3"},
        }
        
        # Storage
        self.seats: Dict[str, List[Seat]] = {}
        self.tickets: Dict[str, Ticket] = {}
        self.showtimes: Dict[str, List[Showtime]] = {}
        
        # Initialize seats
        self._initialize_seats()
        
        self.logger.info("Ticketing system initialized")
    
    def _initialize_seats(self):
        """Initialize all theater seats."""
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        for theater_id, config in self.theaters.items():
            self.seats[theater_id] = []
            
            for row_idx in range(config["rows"]):
                row_letter = rows[row_idx]
                for seat_num in range(1, config["seats_per_row"] + 1):
                    seat_id = f"{theater_id}_{row_letter}{seat_num}"
                    
                    # Calculate 3D position (rows go back, seats go left to right)
                    x = (seat_num - config["seats_per_row"] / 2) * 1.2
                    z = -row_idx * 1.5 - 5
                    y = 0.5
                    
                    # Premium seats (middle rows, middle seats)
                    is_premium = (3 <= row_idx <= 6) and (3 <= seat_num <= 7)
                    
                    seat = Seat(
                        seat_id=seat_id,
                        theater_id=theater_id,
                        row=row_letter,
                        number=seat_num,
                        is_premium=is_premium,
                        position=[x, y, z]
                    )
                    
                    self.seats[theater_id].append(seat)
    
    def create_showtime(
        self,
        project: Project,
        theater_id: str,
        start_time: datetime,
        is_premiere: bool = False
    ) -> Showtime:
        """
        Create a showtime for a movie.
        
        Args:
            project: The project/movie
            theater_id: Theater ID
            start_time: Start time for the showing
            is_premiere: Whether this is a premiere event
            
        Returns:
            Created showtime
        """
        showtime_id = str(uuid.uuid4())
        
        showtime = Showtime(
            showtime_id=showtime_id,
            project_id=project.id,
            theater_id=theater_id,
            start_time=start_time,
            is_premiere=is_premiere
        )
        
        if project.id not in self.showtimes:
            self.showtimes[project.id] = []
        
        self.showtimes[project.id].append(showtime)
        
        self.logger.info(f"Created showtime for {project.title} at {start_time}")
        return showtime
    
    def get_available_seats(self, theater_id: str, showtime_id: Optional[str] = None) -> List[Seat]:
        """
        Get available seats for a theater.
        
        Args:
            theater_id: Theater ID
            showtime_id: Optional showtime ID for specific showing
            
        Returns:
            List of available seats
        """
        if theater_id not in self.seats:
            return []
        
        return [seat for seat in self.seats[theater_id] if not seat.is_reserved]
    
    def purchase_ticket(
        self,
        project_id: str,
        theater_id: str,
        seat_id: str,
        showtime: Showtime,
        purchaser: str = "player"
    ) -> Optional[Ticket]:
        """
        Purchase a ticket for a seat.
        
        Args:
            project_id: Project ID
            theater_id: Theater ID
            seat_id: Seat ID
            showtime: Showtime object
            purchaser: Who is purchasing ("player" or NPC ID)
            
        Returns:
            Ticket if successful, None if seat taken
        """
        # Find the seat
        seat = None
        for s in self.seats[theater_id]:
            if s.seat_id == seat_id:
                seat = s
                break
        
        if not seat or seat.is_reserved:
            self.logger.warning(f"Seat {seat_id} not available")
            return None
        
        # Reserve the seat
        seat.is_reserved = True
        seat.reserved_by = purchaser
        
        # Create ticket
        ticket_id = str(uuid.uuid4())
        
        ticket = Ticket(
            ticket_id=ticket_id,
            project_id=project_id,
            project_title=showtime.project_id,  # Will be updated with actual title
            theater_id=theater_id,
            seat_id=seat_id,
            showtime=showtime.start_time,
            purchased_by=purchaser,
            price=15.00 if seat.is_premium else 12.50
        )
        
        self.tickets[ticket_id] = ticket
        
        self.logger.info(f"Ticket purchased: {seat_id} for {purchaser}")
        return ticket
    
    def validate_ticket(self, ticket_id: str) -> bool:
        """
        Validate and use a ticket.
        
        Args:
            ticket_id: Ticket ID
            
        Returns:
            True if valid and unused
        """
        if ticket_id not in self.tickets:
            return False
        
        ticket = self.tickets[ticket_id]
        
        if ticket.is_used:
            return False
        
        ticket.is_used = True
        return True
    
    def release_seat(self, seat_id: str, theater_id: str):
        """
        Release a reserved seat.
        
        Args:
            seat_id: Seat ID
            theater_id: Theater ID
        """
        for seat in self.seats[theater_id]:
            if seat.seat_id == seat_id:
                seat.is_reserved = False
                seat.reserved_by = None
                break
    
    def get_seat_map(self, theater_id: str) -> Dict:
        """
        Get seat map for display.
        
        Args:
            theater_id: Theater ID
            
        Returns:
            Seat map data
        """
        if theater_id not in self.seats:
            return {}
        
        rows = {}
        for seat in self.seats[theater_id]:
            if seat.row not in rows:
                rows[seat.row] = []
            
            rows[seat.row].append({
                "seat_id": seat.seat_id,
                "number": seat.number,
                "is_reserved": seat.is_reserved,
                "is_premium": seat.is_premium,
                "position": seat.position
            })
        
        return {
            "theater_id": theater_id,
            "theater_name": self.theaters[theater_id]["name"],
            "rows": rows
        }
    
    def generate_showtimes_for_week(self, project: Project):
        """
        Generate showtimes for a week.
        
        Args:
            project: Project to create showtimes for
        """
        if not project.is_released:
            return
        
        # Generate showtimes for next 7 days
        for day in range(7):
            for theater_id in self.theaters.keys():
                # Multiple showtimes per day
                for hour in [14, 17, 20]:  # 2pm, 5pm, 8pm
                    start_time = datetime.now() + timedelta(days=day, hours=hour)
                    self.create_showtime(project, theater_id, start_time)
