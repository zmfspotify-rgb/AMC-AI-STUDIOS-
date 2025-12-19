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
    
    # Assets
    poster_path: Optional[str] = None
    trailer_path: Optional[str] = None
    final_video_path: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    release_date: Optional[datetime] = None


class NPCState(BaseModel):
    """State of an NPC in the theater."""
    id: str
    name: str
    position: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    current_action: str = "idle"
    target_location: Optional[str] = None
    movie_watching: Optional[str] = None
    emotional_state: str = "neutral"
    has_ticket: bool = False
    has_concessions: bool = False
