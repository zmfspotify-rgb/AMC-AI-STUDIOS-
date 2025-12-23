"""Pipeline orchestrator for managing all AI production pipelines."""

import logging
import uuid
from pathlib import Path
from typing import Dict, Optional, List
import json
from datetime import datetime

from src.core.config import Config
from src.models.schema import Project, ProjectType, PipelineStatus
from src.pipelines.script_pipeline import ScriptPipeline
from src.pipelines.casting_pipeline import CastingPipeline
from src.pipelines.filming_pipeline import FilmingPipeline
from src.pipelines.post_production_pipeline import PostProductionPipeline
from src.pipelines.marketing_pipeline import MarketingPipeline


class PipelineOrchestrator:
    """Orchestrates all AI pipelines for movie/TV production."""
    
    def __init__(self, config: Config):
        """
        Initialize the pipeline orchestrator.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = logging.getLogger("AMCStudios.Orchestrator")
        
        # Initialize individual pipelines
        self.script_pipeline = ScriptPipeline(config)
        self.casting_pipeline = CastingPipeline(config)
        self.filming_pipeline = FilmingPipeline(config)
        self.post_production_pipeline = PostProductionPipeline(config)
        self.marketing_pipeline = MarketingPipeline(config)
        
        # Active projects cache
        self.projects: Dict[str, Project] = {}
        
        # Load existing projects
        self._load_projects()
    
    def create_project(
        self,
        title: str,
        story_summary: str,
        project_type: ProjectType,
        genres: List[str],
        rating: str,
        runtime_minutes: Optional[int] = None,
        num_seasons: Optional[int] = None,
        num_episodes: Optional[int] = None,
        tone: str = "balanced"
    ) -> Project:
        """
        Create a new production project.
        
        Args:
            title: Project title
            story_summary: Story description
            project_type: Type of project (film or TV)
            genres: List of genres
            rating: Content rating
            runtime_minutes: Runtime for films
            num_seasons: Number of seasons for TV
            num_episodes: Number of episodes per season for TV
            tone: Tone of the production
            
        Returns:
            Created project
        """
        self.logger.info(f"Creating new project: {title}")
        
        project_id = str(uuid.uuid4())
        
        project = Project(
            id=project_id,
            title=title,
            project_type=project_type,
            genres=genres,
            rating=rating,
            story_summary=story_summary,
            tone=tone,
            runtime_minutes=runtime_minutes,
            num_seasons=num_seasons,
            num_episodes=num_episodes
        )
        
        # Save project
        self.projects[project_id] = project
        self._save_project(project)
        
        self.logger.info(f"Project created with ID: {project_id}")
        return project
    
    def run_full_pipeline(self, project_id: str) -> bool:
        """
        Run the complete production pipeline for a project.
        
        Args:
            project_id: ID of the project
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Starting full pipeline for project: {project_id}")
        
        project = self.projects.get(project_id)
        if not project:
            self.logger.error(f"Project not found: {project_id}")
            return False
        
        try:
            # 1. Script Generation
            self.logger.info("Stage 1: Script Generation")
            project.status["script"] = PipelineStatus.IN_PROGRESS
            self._save_project(project)
            
            script = self.script_pipeline.generate_script(project)
            project.script = script
            project.status["script"] = PipelineStatus.COMPLETED
            self._save_project(project)
            
            # 2. Casting
            self.logger.info("Stage 2: Casting")
            project.status["casting"] = PipelineStatus.IN_PROGRESS
            self._save_project(project)
            
            self.casting_pipeline.cast_project(project)
            project.status["casting"] = PipelineStatus.COMPLETED
            self._save_project(project)
            
            # 3. Filming
            self.logger.info("Stage 3: Filming")
            project.status["filming"] = PipelineStatus.IN_PROGRESS
            self._save_project(project)
            
            self.filming_pipeline.film_project(project)
            project.status["filming"] = PipelineStatus.COMPLETED
            self._save_project(project)
            
            # 4. Post-Production
            self.logger.info("Stage 4: Post-Production")
            project.status["post_production"] = PipelineStatus.IN_PROGRESS
            self._save_project(project)
            
            final_video = self.post_production_pipeline.edit_project(project)
            project.final_video_path = final_video
            project.status["post_production"] = PipelineStatus.COMPLETED
            self._save_project(project)
            
            # 5. Marketing
            self.logger.info("Stage 5: Marketing")
            project.status["marketing"] = PipelineStatus.IN_PROGRESS
            self._save_project(project)
            
            self.marketing_pipeline.create_marketing_materials(project)
            project.status["marketing"] = PipelineStatus.COMPLETED
            
            # 6. Release
            project.status["release"] = PipelineStatus.COMPLETED
            project.release_date = datetime.now()
            self._save_project(project)
            
            self.logger.info(f"Full pipeline completed for: {project.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}", exc_info=True)
            return False
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return self.projects.get(project_id)
    
    def list_projects(self) -> List[Project]:
        """List all projects."""
        return list(self.projects.values())
    
    def _save_project(self, project: Project):
        """Save project to disk."""
        project_dir = self.config.projects_dir / project.id
        project_dir.mkdir(parents=True, exist_ok=True)
        
        project_file = project_dir / "project.json"
        
        # Update timestamp
        project.updated_at = datetime.now()
        
        with open(project_file, 'w') as f:
            json.dump(project.model_dump(mode='json'), f, indent=2, default=str)
    
    def _load_projects(self):
        """Load existing projects from disk."""
        if not self.config.projects_dir.exists():
            return
        
        for project_dir in self.config.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue
            
            project_file = project_dir / "project.json"
            if not project_file.exists():
                continue
            
            try:
                with open(project_file, 'r') as f:
                    project_data = json.load(f)
                    project = Project(**project_data)
                    self.projects[project.id] = project
                    self.logger.info(f"Loaded project: {project.title}")
            except Exception as e:
                self.logger.error(f"Failed to load project from {project_dir}: {e}")
