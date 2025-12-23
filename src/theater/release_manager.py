"""Release management system for AMC AI Studios."""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pytz

from src.core.config import Config
from src.models.schema import (
    Project, ReleaseWindow, Trailer, Interview, RedCarpetEvent
)


class ReleaseManager:
    """Manages movie releases, release windows, and time-locked content."""
    
    def __init__(self, config: Config):
        """Initialize release manager."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.Release")
        
        # Storage
        self.trailers: Dict[str, List[Trailer]] = {}
        self.interviews: Dict[str, List[Interview]] = {}
        self.red_carpet_events: Dict[str, RedCarpetEvent] = {}
        
        self.logger.info("Release manager initialized")
    
    def schedule_release(
        self,
        project: Project,
        release_date: datetime,
        digital_delay_days: int = 45
    ):
        """
        Schedule a project release with windows.
        
        Args:
            project: Project to release
            release_date: Theatrical release date
            digital_delay_days: Days before digital release
        """
        # Set release date
        project.release_date = release_date
        project.digital_release_date = release_date + timedelta(days=digital_delay_days)
        project.current_release_window = ReleaseWindow.THEATRICAL
        
        self.logger.info(f"Scheduled {project.title} for release: {release_date}")
    
    def check_release_unlock(self, project: Project) -> bool:
        """
        Check if project should be unlocked for viewing.
        
        Args:
            project: Project to check
            
        Returns:
            True if unlocked
        """
        if not project.release_date:
            return False
        
        now = datetime.now(pytz.UTC)
        
        # Make release_date timezone-aware if it isn't
        release_date = project.release_date
        if release_date.tzinfo is None:
            release_date = pytz.UTC.localize(release_date)
        
        if now >= release_date and not project.is_released:
            project.is_released = True
            self.logger.info(f"{project.title} is now released!")
            return True
        
        return project.is_released
    
    def get_release_status(self, project: Project) -> Dict:
        """
        Get release status information.
        
        Args:
            project: Project to check
            
        Returns:
            Release status dict
        """
        if not project.release_date:
            return {
                "status": "not_scheduled",
                "message": "No release date set"
            }
        
        now = datetime.now(pytz.UTC)
        release_date = project.release_date
        if release_date.tzinfo is None:
            release_date = pytz.UTC.localize(release_date)
        
        if now < release_date:
            time_until = release_date - now
            return {
                "status": "coming_soon",
                "message": f"Releases in {time_until.days} days, {time_until.seconds // 3600} hours",
                "countdown": {
                    "days": time_until.days,
                    "hours": time_until.seconds // 3600,
                    "minutes": (time_until.seconds % 3600) // 60
                }
            }
        
        # Check digital release
        if project.digital_release_date:
            digital_date = project.digital_release_date
            if digital_date.tzinfo is None:
                digital_date = pytz.UTC.localize(digital_date)
            
            if now < digital_date:
                return {
                    "status": "theatrical",
                    "message": "In theaters now",
                    "window": "theatrical"
                }
            else:
                return {
                    "status": "digital",
                    "message": "Available for streaming",
                    "window": "digital"
                }
        
        return {
            "status": "released",
            "message": "Released",
            "window": "theatrical"
        }
    
    def get_available_content(self, project: Project) -> Dict:
        """
        Get what content is available based on release windows.
        
        Args:
            project: Project to check
            
        Returns:
            Available content dict
        """
        status = self.get_release_status(project)
        
        content = {
            "trailer": project.trailer_path,
            "poster": project.poster_path,
            "full_movie": None,
            "interviews": [],
            "can_purchase_tickets": False
        }
        
        if status["status"] == "coming_soon":
            # Only trailers and posters
            content["interviews"] = self.get_project_interviews(project.id)
        elif status["status"] == "theatrical":
            # Can watch in theater only
            content["full_movie"] = project.theatrical_cut_path or project.final_video_path
            content["can_purchase_tickets"] = True
            content["interviews"] = self.get_project_interviews(project.id)
        elif status["status"] == "digital":
            # Can watch anywhere
            content["full_movie"] = project.home_cut_path or project.final_video_path
            content["can_purchase_tickets"] = False
            content["interviews"] = self.get_project_interviews(project.id)
        
        return content
    
    def add_trailer(self, trailer: Trailer):
        """Add a trailer for a project."""
        if trailer.project_id not in self.trailers:
            self.trailers[trailer.project_id] = []
        
        self.trailers[trailer.project_id].append(trailer)
        self.logger.info(f"Added trailer for project {trailer.project_id}")
    
    def get_project_trailers(self, project_id: str) -> List[Trailer]:
        """Get all trailers for a project."""
        return self.trailers.get(project_id, [])
    
    def add_interview(self, interview: Interview):
        """Add an interview for a project."""
        if interview.project_id not in self.interviews:
            self.interviews[interview.project_id] = []
        
        self.interviews[interview.project_id].append(interview)
        self.logger.info(f"Added interview for project {interview.project_id}")
    
    def get_project_interviews(self, project_id: str) -> List[Interview]:
        """Get all interviews for a project."""
        return self.interviews.get(project_id, [])
    
    def schedule_red_carpet(
        self,
        project: Project,
        event_time: Optional[datetime] = None,
        attending_actors: List[str] = []
    ) -> RedCarpetEvent:
        """
        Schedule a red carpet premiere event.
        
        Args:
            project: Project for premiere
            event_time: Event time (defaults to 1 hour before release)
            attending_actors: List of actor IDs attending
            
        Returns:
            Created red carpet event
        """
        import uuid
        
        if not event_time and project.release_date:
            event_time = project.release_date - timedelta(hours=1)
        elif not event_time:
            event_time = datetime.now() + timedelta(hours=1)
        
        event = RedCarpetEvent(
            event_id=str(uuid.uuid4()),
            project_id=project.id,
            event_time=event_time,
            attending_actors=attending_actors
        )
        
        self.red_carpet_events[project.id] = event
        self.logger.info(f"Scheduled red carpet for {project.title}")
        
        return event
    
    def check_red_carpet_active(self, project_id: str) -> Optional[RedCarpetEvent]:
        """
        Check if red carpet event is currently active.
        
        Args:
            project_id: Project ID
            
        Returns:
            Active event or None
        """
        if project_id not in self.red_carpet_events:
            return None
        
        event = self.red_carpet_events[project_id]
        now = datetime.now(pytz.UTC)
        
        event_time = event.event_time
        if event_time.tzinfo is None:
            event_time = pytz.UTC.localize(event_time)
        
        event_end = event_time + timedelta(minutes=event.duration)
        
        if event_time <= now <= event_end and not event.is_completed:
            event.is_active = True
            return event
        elif now > event_end:
            event.is_active = False
            event.is_completed = True
            event.replay_available = True
        
        return None if not event.is_active else event
