"""Web-based UI server for AMC AI Studios."""

import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time
from pathlib import Path
from datetime import datetime

from src.core.config import Config
from src.pipelines.orchestrator import PipelineOrchestrator
from src.pipelines.slate_manager import StudioSlateManager
from src.theater.theater_manager import TheaterManager
from src.models.schema import ProjectType


class UIServer:
    """Flask-based UI server."""
    
    def __init__(
        self,
        config: Config,
        orchestrator: PipelineOrchestrator,
        theater_manager: TheaterManager,
        slate_manager: StudioSlateManager
    ):
        """Initialize UI server."""
        self.config = config
        self.orchestrator = orchestrator
        self.theater_manager = theater_manager
        self.slate_manager = slate_manager
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
        
        # Studio Slate Management
        @self.app.route('/api/slate', methods=['GET'])
        def get_slate():
            """Get studio slate overview."""
            return jsonify(self.slate_manager.get_slate_overview())
        
        @self.app.route('/api/slate/statistics', methods=['GET'])
        def get_studio_stats():
            """Get studio statistics."""
            return jsonify(self.slate_manager.get_studio_statistics())
        
        @self.app.route('/api/projects/<project_id>/production/start', methods=['POST'])
        def start_production(project_id):
            """Start production on a project."""
            success = self.slate_manager.start_production(project_id)
            return jsonify({"success": success})
        
        @self.app.route('/api/projects/<project_id>/production/status', methods=['GET'])
        def get_production_status(project_id):
            """Get production status."""
            return jsonify(self.slate_manager.get_production_status(project_id))
        
        # Ticketing
        @self.app.route('/api/ticketing/theaters', methods=['GET'])
        def get_theaters():
            """Get theater configurations."""
            return jsonify({
                theater_id: {
                    "id": theater_id,
                    "name": config["name"],
                    "rows": config["rows"],
                    "seats_per_row": config["seats_per_row"]
                }
                for theater_id, config in self.theater_manager.ticketing.theaters.items()
            })
        
        @self.app.route('/api/ticketing/seat-map/<theater_id>', methods=['GET'])
        def get_seat_map(theater_id):
            """Get seat map for a theater."""
            return jsonify(self.theater_manager.ticketing.get_seat_map(theater_id))
        
        @self.app.route('/api/ticketing/showtimes/<project_id>', methods=['GET'])
        def get_showtimes(project_id):
            """Get showtimes for a project."""
            showtimes = self.theater_manager.ticketing.showtimes.get(project_id, [])
            return jsonify([
                {
                    "showtime_id": s.showtime_id,
                    "theater_id": s.theater_id,
                    "start_time": s.start_time.isoformat(),
                    "is_premiere": s.is_premiere
                }
                for s in showtimes
            ])
        
        @self.app.route('/api/ticketing/purchase', methods=['POST'])
        def purchase_ticket():
            """Purchase a ticket."""
            data = request.json
            
            # Get showtime
            showtimes = self.theater_manager.ticketing.showtimes.get(data['project_id'], [])
            showtime = next((s for s in showtimes if s.showtime_id == data['showtime_id']), None)
            
            if not showtime:
                return jsonify({"error": "Showtime not found"}), 404
            
            ticket = self.theater_manager.ticketing.purchase_ticket(
                data['project_id'],
                data['theater_id'],
                data['seat_id'],
                showtime,
                "player"
            )
            
            if ticket:
                return jsonify({
                    "success": True,
                    "ticket": ticket.model_dump(mode='json')
                })
            else:
                return jsonify({"error": "Seat not available"}), 400
        
        # Release Management
        @self.app.route('/api/release/<project_id>/status', methods=['GET'])
        def get_release_status(project_id):
            """Get release status for a project."""
            project = self.orchestrator.get_project(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404
            
            return jsonify(self.theater_manager.release_manager.get_release_status(project))
        
        @self.app.route('/api/release/<project_id>/content', methods=['GET'])
        def get_available_content(project_id):
            """Get available content based on release window."""
            project = self.orchestrator.get_project(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404
            
            return jsonify(self.theater_manager.release_manager.get_available_content(project))
        
        @self.app.route('/api/release/<project_id>/schedule', methods=['POST'])
        def schedule_release(project_id):
            """Schedule a release date."""
            data = request.json
            project = self.orchestrator.get_project(project_id)
            
            if not project:
                return jsonify({"error": "Project not found"}), 404
            
            release_date = datetime.fromisoformat(data['release_date'])
            self.theater_manager.release_manager.schedule_release(
                project,
                release_date,
                data.get('digital_delay_days', 45)
            )
            
            return jsonify({"success": True})
        
        # Red Carpet Events
        @self.app.route('/api/red-carpet/<project_id>/schedule', methods=['POST'])
        def schedule_red_carpet(project_id):
            """Schedule a red carpet event."""
            data = request.json
            project = self.orchestrator.get_project(project_id)
            
            if not project:
                return jsonify({"error": "Project not found"}), 404
            
            event_time = None
            if 'event_time' in data:
                event_time = datetime.fromisoformat(data['event_time'])
            
            event = self.theater_manager.release_manager.schedule_red_carpet(
                project,
                event_time,
                data.get('attending_actors', [])
            )
            
            return jsonify(event.model_dump(mode='json'))
        
        @self.app.route('/api/red-carpet/<project_id>/active', methods=['GET'])
        def check_red_carpet_active(project_id):
            """Check if red carpet event is active."""
            event = self.theater_manager.release_manager.check_red_carpet_active(project_id)
            
            if event:
                return jsonify(event.model_dump(mode='json'))
            else:
                return jsonify({"active": False})
        
        # NPC Reviews and Analytics
        @self.app.route('/api/reviews/<project_id>', methods=['GET'])
        def get_project_reviews(project_id):
            """Get NPC reviews for a project."""
            reviews = self.theater_manager.npc_intelligence.reviews.get(project_id, [])
            return jsonify([r.model_dump(mode='json') for r in reviews])
        
        @self.app.route('/api/analytics/<project_id>', methods=['GET'])
        def get_project_analytics(project_id):
            """Get project analytics."""
            project = self.orchestrator.get_project(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404
            
            return jsonify(self.theater_manager.npc_intelligence.get_project_analytics(project))
        
        @self.app.route('/api/analytics/trending', methods=['GET'])
        def get_trending():
            """Get trending projects."""
            return jsonify(self.theater_manager.npc_intelligence.get_trending_projects())
        
        @self.app.route('/api/analytics/<project_id>/sequel', methods=['GET'])
        def check_sequel_greenlight(project_id):
            """Check if project should get a sequel."""
            project = self.orchestrator.get_project(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404
            
            return jsonify(self.theater_manager.npc_intelligence.should_greenlight_sequel(project))
        
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
