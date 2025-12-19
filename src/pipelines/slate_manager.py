"""Studio Slate Manager for handling multiple concurrent projects."""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import threading

from src.core.config import Config
from src.models.schema import Project, ProjectStatus, PipelineStatus
from src.pipelines.orchestrator import PipelineOrchestrator


class StudioSlateManager:
    """Manages multiple projects in parallel like a real studio slate."""
    
    def __init__(self, config: Config, orchestrator: PipelineOrchestrator):
        """Initialize slate manager."""
        self.config = config
        self.orchestrator = orchestrator
        self.logger = logging.getLogger("AMCStudios.SlateManager")
        
        # Active production threads
        self.active_productions: Dict[str, threading.Thread] = {}
        
        # Job queue
        self.job_queue: List[str] = []
        
        # Resource limits
        self.max_concurrent_productions = 5
        
        self.logger.info("Studio Slate Manager initialized")
    
    def get_slate_overview(self) -> Dict:
        """
        Get overview of all projects in the studio slate.
        
        Returns:
            Categorized project dict
        """
        slate = {
            "in_development": [],
            "in_production": [],
            "in_post": [],
            "marketing": [],
            "released": [],
            "total_projects": len(self.orchestrator.projects)
        }
        
        for project in self.orchestrator.projects.values():
            project_info = {
                "id": project.id,
                "title": project.title,
                "type": project.project_type,
                "genres": project.genres,
                "status": project.project_status,
                "pipeline_progress": self._get_pipeline_progress(project),
                "average_rating": project.average_rating,
                "box_office": project.box_office_total
            }
            
            # Categorize by status
            if project.project_status == ProjectStatus.IN_DEVELOPMENT:
                slate["in_development"].append(project_info)
            elif project.project_status == ProjectStatus.IN_PRODUCTION:
                slate["in_production"].append(project_info)
            elif project.project_status == ProjectStatus.IN_POST:
                slate["in_post"].append(project_info)
            elif project.project_status == ProjectStatus.MARKETING:
                slate["marketing"].append(project_info)
            elif project.project_status == ProjectStatus.RELEASED:
                slate["released"].append(project_info)
        
        return slate
    
    def _get_pipeline_progress(self, project: Project) -> Dict:
        """Get pipeline progress percentage."""
        stages = ["script", "casting", "filming", "post_production", "marketing"]
        completed = sum(
            1 for stage in stages 
            if project.status.get(stage) == PipelineStatus.COMPLETED
        )
        
        return {
            "completed_stages": completed,
            "total_stages": len(stages),
            "percentage": (completed / len(stages)) * 100,
            "current_stage": self._get_current_stage(project)
        }
    
    def _get_current_stage(self, project: Project) -> str:
        """Determine current stage of production."""
        if project.status.get("marketing") == PipelineStatus.IN_PROGRESS:
            return "Marketing"
        elif project.status.get("post_production") == PipelineStatus.IN_PROGRESS:
            return "Post-Production"
        elif project.status.get("filming") == PipelineStatus.IN_PROGRESS:
            return "Filming"
        elif project.status.get("casting") == PipelineStatus.IN_PROGRESS:
            return "Casting"
        elif project.status.get("script") == PipelineStatus.IN_PROGRESS:
            return "Script Development"
        else:
            return "Development"
    
    def start_production(self, project_id: str) -> bool:
        """
        Start production on a project in background.
        
        Args:
            project_id: Project to start
            
        Returns:
            True if started
        """
        if project_id in self.active_productions:
            self.logger.warning(f"Project {project_id} already in production")
            return False
        
        if len(self.active_productions) >= self.max_concurrent_productions:
            self.logger.info(f"Production queue full, adding {project_id} to queue")
            self.job_queue.append(project_id)
            return True
        
        # Start production thread
        thread = threading.Thread(
            target=self._run_production,
            args=(project_id,),
            daemon=True
        )
        thread.start()
        
        self.active_productions[project_id] = thread
        
        project = self.orchestrator.projects[project_id]
        project.project_status = ProjectStatus.IN_PRODUCTION
        
        self.logger.info(f"Started production on {project.title}")
        return True
    
    def _run_production(self, project_id: str):
        """Run the production pipeline for a project."""
        try:
            self.logger.info(f"Running pipeline for project {project_id}")
            success = self.orchestrator.run_full_pipeline(project_id)
            
            if success:
                project = self.orchestrator.projects[project_id]
                project.project_status = ProjectStatus.MARKETING
                self.logger.info(f"Pipeline complete for {project.title}")
            
        except Exception as e:
            self.logger.error(f"Production failed for {project_id}: {e}", exc_info=True)
        
        finally:
            # Remove from active
            if project_id in self.active_productions:
                del self.active_productions[project_id]
            
            # Start next in queue
            self._start_next_in_queue()
    
    def _start_next_in_queue(self):
        """Start next project in queue if space available."""
        if self.job_queue and len(self.active_productions) < self.max_concurrent_productions:
            next_project_id = self.job_queue.pop(0)
            self.start_production(next_project_id)
    
    def cancel_production(self, project_id: str) -> bool:
        """
        Cancel an active production.
        
        Args:
            project_id: Project to cancel
            
        Returns:
            True if canceled
        """
        if project_id in self.active_productions:
            # Note: Can't actually stop thread, but can mark as canceled
            self.logger.info(f"Production canceled for {project_id}")
            # Thread will finish but project won't be updated
            return True
        elif project_id in self.job_queue:
            self.job_queue.remove(project_id)
            return True
        
        return False
    
    def get_production_status(self, project_id: str) -> Dict:
        """
        Get detailed production status.
        
        Args:
            project_id: Project ID
            
        Returns:
            Status dict
        """
        if project_id not in self.orchestrator.projects:
            return {"error": "Project not found"}
        
        project = self.orchestrator.projects[project_id]
        
        status = {
            "project_id": project_id,
            "title": project.title,
            "project_status": project.project_status,
            "pipeline_status": project.status,
            "is_active": project_id in self.active_productions,
            "in_queue": project_id in self.job_queue,
            "queue_position": self.job_queue.index(project_id) + 1 if project_id in self.job_queue else None,
            "progress": self._get_pipeline_progress(project)
        }
        
        return status
    
    def get_studio_statistics(self) -> Dict:
        """
        Get overall studio statistics.
        
        Returns:
            Statistics dict
        """
        total_projects = len(self.orchestrator.projects)
        
        stats = {
            "total_projects": total_projects,
            "active_productions": len(self.active_productions),
            "queued_projects": len(self.job_queue),
            "capacity_remaining": self.max_concurrent_productions - len(self.active_productions),
            "projects_by_status": {},
            "total_box_office": 0.0,
            "average_rating": 0.0
        }
        
        # Count by status
        for status in ProjectStatus:
            stats["projects_by_status"][status.value] = sum(
                1 for p in self.orchestrator.projects.values()
                if p.project_status == status
            )
        
        # Calculate totals
        if total_projects > 0:
            total_box_office = sum(p.box_office_total for p in self.orchestrator.projects.values())
            stats["total_box_office"] = total_box_office
            
            rated_projects = [p for p in self.orchestrator.projects.values() if p.average_rating > 0]
            if rated_projects:
                stats["average_rating"] = sum(p.average_rating for p in rated_projects) / len(rated_projects)
        
        return stats
