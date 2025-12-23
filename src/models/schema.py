"""Data models for AMC AI Studios."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ProjectType(str, Enum):
    """Type of production project."""
    FEATURE_FILM = "feature_film"
    TV_SHOW = "tv_show"


class Rating(str, Enum):
    """Content rating."""
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    TV_MA = "TV-MA"


class Genre(str, Enum):
    """Movie/TV genres."""
    ACTION = "Action"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    HORROR = "Horror"
    SCIFI = "Sci-Fi"
    FANTASY = "Fantasy"
    THRILLER = "Thriller"
    ROMANCE = "Romance"
    MYSTERY = "Mystery"
    ADVENTURE = "Adventure"


class PipelineStatus(str, Enum):
    """Status of a pipeline stage."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectStatus(str, Enum):
    """Overall project status in studio slate."""
    IN_DEVELOPMENT = "in_development"
    IN_PRODUCTION = "in_production"
    IN_POST = "in_post"
    MARKETING = "marketing"
    RELEASED = "released"
    ARCHIVED = "archived"


class ReleaseWindow(str, Enum):
    """Release window type."""
    THEATRICAL = "theatrical"
    DIGITAL = "digital"
    STREAMING = "streaming"
    ARCHIVE = "archive"


class CutType(str, Enum):
    """Type of movie cut."""
    THEATRICAL = "theatrical"
    EXTENDED = "extended"
    DIRECTORS = "directors"
    HOME = "home"


class ActorProfile(BaseModel):
    """AI Actor profile with persistent identity."""
    id: str
    name: str
    age: int
    gender: str
    ethnicity: str
    facial_embedding: Optional[List[float]] = None
    voice_profile_path: Optional[str] = None
    body_type: str = "average"
    acting_style: str = "method"
    emotional_range: List[str] = Field(default_factory=list)
    career_history: List[str] = Field(default_factory=list)
    avatar_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Character(BaseModel):
    """Character in a production."""
    name: str
    description: str
    role: str  # protagonist, antagonist, supporting, etc.
    personality_traits: List[str] = Field(default_factory=list)
    emotional_arc: Optional[str] = None
    assigned_actor_id: Optional[str] = None


class SceneMetadata(BaseModel):
    """Metadata for a scene."""
    scene_number: int
    location: str
    time_of_day: str
    characters: List[str]
    required_emotions: List[str] = Field(default_factory=list)
    camera_style: str = "standard"
    lighting_mood: str = "neutral"
    description: str = ""


class Scene(BaseModel):
    """A scene in the screenplay."""
    scene_number: int
    scene_type: str  # INT. or EXT.
    location: str
    time: str
    action: str
    dialogue: List[Dict[str, str]] = Field(default_factory=list)  # [{"character": "name", "line": "text"}]
    metadata: Optional[SceneMetadata] = None
    video_path: Optional[str] = None
    takes: List[str] = Field(default_factory=list)


class Script(BaseModel):
    """Complete screenplay."""
    title: str
    version: str = "Draft 1"
    logline: str = ""
    scenes: List[Scene] = Field(default_factory=list)
    characters: List[Character] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Project(BaseModel):
    """Main production project."""
    id: str
    title: str
    project_type: ProjectType
    genres: List[Genre]
    rating: Rating
    runtime_minutes: Optional[int] = None
    num_seasons: Optional[int] = None
    num_episodes: Optional[int] = None
    
    # Story
    story_summary: str
    tone: str = "balanced"
    
    # Script
    script: Optional[Script] = None
    
    # Production status
    status: Dict[str, PipelineStatus] = Field(default_factory=lambda: {
        "script": PipelineStatus.PENDING,
        "casting": PipelineStatus.PENDING,
        "filming": PipelineStatus.PENDING,
        "post_production": PipelineStatus.PENDING,
        "marketing": PipelineStatus.PENDING,
        "release": PipelineStatus.PENDING,
    })
    
    # Project status in studio slate
    project_status: ProjectStatus = ProjectStatus.IN_DEVELOPMENT
    
    # Assets
    poster_path: Optional[str] = None
    trailer_path: Optional[str] = None
    final_video_path: Optional[str] = None
    theatrical_cut_path: Optional[str] = None
    directors_cut_path: Optional[str] = None
    home_cut_path: Optional[str] = None
    
    # Release information
    release_date: Optional[datetime] = None
    digital_release_date: Optional[datetime] = None
    current_release_window: ReleaseWindow = ReleaseWindow.THEATRICAL
    is_released: bool = False
    
    # Box office and performance
    box_office_total: float = 0.0
    npc_reviews: List[Dict[str, Any]] = Field(default_factory=list)
    average_rating: float = 0.0
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class NPCState(BaseModel):
    """State of an NPC in the theater."""
    id: str
    name: str
    position: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    rotation: float = 0.0  # Y-axis rotation in radians
    current_action: str = "idle"
    target_location: Optional[str] = None
    movie_watching: Optional[str] = None
    emotional_state: str = "neutral"
    has_ticket: bool = False
    has_concessions: bool = False
    seat_number: Optional[str] = None
    ticket_id: Optional[str] = None


class Seat(BaseModel):
    """Theater seat model."""
    seat_id: str
    theater_id: str
    row: str
    number: int
    is_reserved: bool = False
    reserved_by: Optional[str] = None  # NPC ID or "player"
    is_premium: bool = False
    position: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])


class Ticket(BaseModel):
    """Movie ticket model."""
    ticket_id: str
    project_id: str
    project_title: str
    theater_id: str
    seat_id: str
    showtime: datetime
    purchased_at: datetime = Field(default_factory=datetime.now)
    purchased_by: str  # "player" or NPC ID
    price: float = 12.50
    is_used: bool = False


class Showtime(BaseModel):
    """Movie showtime."""
    showtime_id: str
    project_id: str
    theater_id: str
    start_time: datetime
    trailers_duration: int = 15  # minutes
    is_premiere: bool = False


class Trailer(BaseModel):
    """Trailer asset."""
    trailer_id: str
    project_id: str
    title: str
    duration: int  # seconds
    video_path: str
    thumbnail_path: Optional[str] = None
    trailer_type: str = "teaser"  # teaser, official, final
    created_at: datetime = Field(default_factory=datetime.now)


class Interview(BaseModel):
    """AI-generated interview content."""
    interview_id: str
    project_id: str
    title: str
    interviewer_name: str
    interviewer_personality: str  # serious, funny, chaotic, fan-focused
    actors: List[str]  # Actor IDs
    content_path: str
    interview_type: str  # sit-down, late-night, game, roundtable, behind-the-scenes
    duration: int  # seconds
    created_at: datetime = Field(default_factory=datetime.now)


class RedCarpetEvent(BaseModel):
    """Red carpet premiere event."""
    event_id: str
    project_id: str
    event_time: datetime
    duration: int = 60  # minutes
    attending_actors: List[str]  # Actor IDs
    is_active: bool = False
    is_completed: bool = False
    replay_available: bool = False
    replay_path: Optional[str] = None


class NPCReview(BaseModel):
    """NPC review of a movie."""
    review_id: str
    npc_id: str
    npc_name: str
    project_id: str
    rating: float  # 0-10
    sentiment: str  # positive, negative, mixed
    review_text: str
    emotional_reaction: List[str] = Field(default_factory=list)  # [laugh, gasp, clap, etc.]
    created_at: datetime = Field(default_factory=datetime.now)
