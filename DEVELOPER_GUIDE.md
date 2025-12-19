# AMC AI Studios - Developer Guide

## Project Overview

AMC AI Studios is a comprehensive AI-powered movie and television production system that demonstrates a complete entertainment creation pipeline from concept to virtual theater release.

## System Architecture

### Core Components

1. **Configuration System** (`src/core/config.py`)
   - Environment-based configuration
   - Directory management
   - API key handling

2. **Data Models** (`src/models/schema.py`)
   - Pydantic models for type safety
   - Project, Script, Scene, Character, ActorProfile
   - NPC state management

3. **AI Pipelines** (`src/pipelines/`)
   - Script Generation: Creates Hollywood-format screenplays
   - Casting: Assigns persistent AI actors to roles
   - Filming: Generates scene metadata and video placeholders
   - Post-Production: Handles editing, color, sound, music
   - Marketing: Creates promotional materials

4. **Theater System** (`src/theater/`)
   - Theater Manager: Coordinates virtual theater state
   - NPC AI: Implements intelligent NPC behaviors

5. **UI System** (`src/ui/`)
   - Flask web server
   - REST API endpoints
   - Responsive web interface

## Key Features

### 1. Persistent AI Actors
AI actors maintain consistent identity across projects:
- Unique ID
- Facial features (embedding)
- Voice profile
- Acting style
- Career history

### 2. Complete Production Pipeline
Full automation from story to release:
```
Story → Script → Casting → Filming → Post → Marketing → Release
```

### 3. Virtual Theater with NPCs
Intelligent NPCs that:
- Navigate the theater
- Make decisions (buy tickets, concessions)
- Watch movies and react emotionally
- Interact with the environment

### 4. Web-Based UI
Modern, cinematic interface with:
- Project creation wizard
- Real-time pipeline monitoring
- Theater state visualization

## Development Setup

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Installation

1. Clone repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate.bat  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.template .env
   # Edit .env with your settings
   ```

5. Run application:
   ```bash
   python main.py
   ```

## API Endpoints

### Projects

**GET /api/projects**
- List all projects

**GET /api/projects/<id>**
- Get project details

**POST /api/projects**
- Create new project
- Body: Project data (title, story, type, etc.)

**POST /api/projects/<id>/run**
- Start AI pipeline for project

### Theater

**GET /api/theater/state**
- Get current theater state and NPCs

**GET /api/theater/now-showing**
- Get available movies in theater

## Data Storage

All data is stored locally in the `data/` directory:

```
data/
├── projects/          # Project files
│   └── <project-id>/
│       ├── project.json
│       └── ...
├── actors/            # AI actor profiles
│   └── <actor-id>.json
├── assets/            # Generated content
│   └── <project-id>/
│       ├── scenes/
│       ├── output/
│       └── marketing/
└── cache/             # Temporary cache
```

## Testing

Run the test script:
```bash
python test_system.py
```

This validates:
- Configuration loading
- Project creation
- Script generation
- Theater initialization
- NPC behaviors

## Building for Distribution

### Windows Executable

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build executable:
   ```bash
   pyinstaller AMC_AI_Studios.spec
   ```
   
   Or use the build script:
   ```bash
   build.bat
   ```

3. Output in `dist/AMC_AI_Studios/`

## AI Integration

### Without API Keys
The system works in "template mode":
- Uses predefined templates for characters
- Generates basic scene structures
- No external API calls

### With API Keys
Enhanced features with OpenAI/Anthropic:
- Creative script generation
- Detailed character development
- Advanced scene descriptions
- Image generation (posters)

### Adding AI Services

1. Set API keys in `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   ```

2. The system automatically uses available services

## Extending the System

### Adding New Pipelines

1. Create pipeline class in `src/pipelines/`
2. Implement required methods
3. Register in `orchestrator.py`

### Adding New NPC Behaviors

1. Edit `src/theater/npc_ai.py`
2. Add new states to state machine
3. Implement behavior logic

### Customizing UI

1. Edit templates: `src/ui/templates/`
2. Update styles: `src/ui/static/css/`
3. Add features: `src/ui/static/js/`

## Performance Considerations

- NPCs update every second (configurable)
- AI calls are cached when possible
- Projects persist to disk incrementally
- Large video files would need optimization

## Security

- API keys stored in `.env` (not committed)
- Local-only by default (Flask on 127.0.0.1)
- No external data transmission except AI APIs

## Troubleshooting

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Port in Use
- Change `FLASK_PORT` in `.env`
- Default is 5000

### AI Not Working
- Check API keys in `.env`
- System works without them in template mode

## Future Enhancements

Potential additions:
- Actual video generation (Stable Diffusion Video)
- Real-time 3D theater rendering
- Voice synthesis integration
- Advanced NPC conversations
- Multi-user support
- Cloud deployment

## Code Style

- PEP 8 compliant
- Type hints where applicable
- Docstrings for all public methods
- Meaningful variable names
- Modular, testable code

## License

All Rights Reserved © 2024 AMC AI Studios
