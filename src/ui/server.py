"""Web-based UI server for AMC AI Studios."""

import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time
from pathlib import Path

from src.core.config import Config
from src.pipelines.orchestrator import PipelineOrchestrator
from src.theater.theater_manager import TheaterManager
from src.models.schema import ProjectType


class UIServer:
    """Flask-based UI server."""
    
    def __init__(
        self,
        config: Config,
        orchestrator: PipelineOrchestrator,
        theater_manager: TheaterManager
    ):
        """Initialize UI server."""
        self.config = config
        self.orchestrator = orchestrator
        self.theater_manager = theater_manager
        self.logger = logging.getLogger("AMCStudios.UI")
        
        # Create Flask app
        self.app = Flask(
            __name__,
            template_folder=str(Path(__file__).parent / "templates"),
            static_folder=str(Path(__file__).parent / "static")
        )
        CORS(self.app)
        
        # Setup routes
        self._setup_routes()
        
        # Background theater update thread
        self.theater_update_thread = None
        self.running = False
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main page."""
            return render_template('index.html', config=self.config)
        
        @self.app.route('/api/projects', methods=['GET'])
        def list_projects():
            """List all projects."""
            projects = self.orchestrator.list_projects()
            return jsonify([
                {
                    "id": p.id,
                    "title": p.title,
                    "type": p.project_type,
                    "status": p.status,
                    "created_at": p.created_at.isoformat()
                }
                for p in projects
            ])
        
        @self.app.route('/api/projects/<project_id>', methods=['GET'])
        def get_project(project_id):
            """Get project details."""
            project = self.orchestrator.get_project(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404
            return jsonify(project.model_dump(mode='json'))
        
        @self.app.route('/api/projects', methods=['POST'])
        def create_project():
            """Create new project."""
            data = request.json
            
            try:
                project = self.orchestrator.create_project(
                    title=data['title'],
                    story_summary=data['story_summary'],
                    project_type=ProjectType(data['project_type']),
                    genres=data.get('genres', []),
                    rating=data['rating'],
                    runtime_minutes=data.get('runtime_minutes'),
                    num_seasons=data.get('num_seasons'),
                    num_episodes=data.get('num_episodes'),
                    tone=data.get('tone', 'balanced')
                )
                
                return jsonify({
                    "success": True,
                    "project_id": project.id
                })
            except Exception as e:
                self.logger.error(f"Failed to create project: {e}")
                return jsonify({"error": str(e)}), 400
        
        @self.app.route('/api/projects/<project_id>/run', methods=['POST'])
        def run_pipeline(project_id):
            """Run full pipeline for a project."""
            
            # Run in background thread
            def run_async():
                self.orchestrator.run_full_pipeline(project_id)
            
            thread = threading.Thread(target=run_async, daemon=True)
            thread.start()
            
            return jsonify({"success": True, "message": "Pipeline started"})
        
        @self.app.route('/api/theater/state', methods=['GET'])
        def get_theater_state():
            """Get current theater state."""
            state = self.theater_manager.get_theater_state()
            return jsonify(state)
        
        @self.app.route('/api/theater/now-showing', methods=['GET'])
        def get_now_showing():
            """Get movies currently showing."""
            return jsonify([
                {
                    "id": p.id,
                    "title": p.title,
                    "rating": p.rating,
                    "genres": p.genres,
                    "runtime": p.runtime_minutes,
                    "poster": p.poster_path
                }
                for p in self.theater_manager.now_showing
            ])
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint."""
            return jsonify({"status": "healthy"})
    
    def run(self):
        """Run the UI server."""
        self.logger.info(f"Starting UI server on {self.config.flask_host}:{self.config.flask_port}")
        
        # Start theater update thread
        self.running = True
        self.theater_update_thread = threading.Thread(
            target=self._update_theater_loop,
            daemon=True
        )
        self.theater_update_thread.start()
        
        # Run Flask app with error handling
        try:
            self.app.run(
                host=self.config.flask_host,
                port=self.config.flask_port,
                debug=self.config.flask_debug,
                use_reloader=False  # Disable reloader to avoid double initialization
            )
        except OSError as e:
            if "Address already in use" in str(e) or "port" in str(e).lower():
                self.logger.error(f"Port {self.config.flask_port} is already in use!")
                self.logger.error("Please either:")
                self.logger.error("  1. Stop the other application using this port")
                self.logger.error("  2. Change FLASK_PORT in your .env file")
                raise
            else:
                raise
    
    def _update_theater_loop(self):
        """Background loop to update theater state."""
        while self.running:
            try:
                self.theater_manager.update(delta_time=1.0)
                time.sleep(1.0)  # Update every second
            except Exception as e:
                self.logger.error(f"Theater update error: {e}")
