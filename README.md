# AMC AI STUDIOS

🎬 **Fully AI-Generated Movie & Television Studio + Virtual AMC Theater**

A complete, functional AI-powered entertainment production system that autonomously creates movies and TV shows from concept to completion, featuring a virtual AMC theater with AI-driven NPCs.

## 🚀 QUICK START (3 EASY WAYS)

### ⭐ METHOD 1: AUTOMATIC LAUNCHER (EASIEST!)

**Windows:**
```bash
Double-click RUN.bat
```

**Mac/Linux:**
```bash
python3 run.py
```

This automatically installs all dependencies and starts the app!
Then open your browser to: **http://localhost:5000**

---

### METHOD 2: Simple Manual Start

```bash
# Install dependencies
pip install python-dotenv pydantic flask flask-cors

# Run the app
python3 main.py

# Open browser to http://localhost:5000
```

---

### METHOD 3: Full Launcher (Windows)

```bash
launch.bat
```

---

## 🎬 What You'll See

Once you open **http://localhost:5000**, you'll see:

- **Create Tab**: Build new movies/TV shows
- **Projects Tab**: Monitor your productions
- **Theater Tab**: Virtual AMC cinema with 20 AI NPCs

---

## 🚀 Features

### Complete AI Production Pipeline
- **Story & Script Generation**: Hollywood-format screenplays with scene breakdowns
- **AI Casting System**: Persistent AI actors with consistent appearance and voice
- **AI Filming Engine**: Scene generation with camera work, lighting, and blocking
- **Post-Production**: Automated editing, color grading, sound design, and music
- **Marketing & Distribution**: Trailers, posters, and promotional materials
- **Virtual Theater**: 3D AMC theater with AI NPCs

### Virtual AMC Theater Experience
- Interactive 3D theater environment
- AI-driven NPCs that:
  - Walk around the theater
  - Buy tickets and concessions
  - Enter screening rooms
  - Watch movies and react (laugh, gasp, clap)
  - Socialize with each other
- "Now Showing" section for completed productions
- Real-time theater state monitoring

## 📋 Requirements

- **Windows 10 or later**
- **Python 3.10+** (for running from source)
- **Optional**: OpenAI API key or Anthropic API key for enhanced AI features

## 🎯 Quick Start

### Option 1: Run from Source (Recommended for Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/zmfspotify-rgb/AMC-AI-STUDIOS-.git
   cd AMC-AI-STUDIOS-
   ```

2. **Configure API Keys (Optional)**
   - Copy `.env.template` to `.env`
   - Add your API keys:
     ```
     OPENAI_API_KEY=your_key_here
     ANTHROPIC_API_KEY=your_key_here
     ```
   - The system works in limited mode without API keys

3. **Launch the Application**
   - Simply double-click `launch.bat`
   - Or run from command line:
     ```bash
     launch.bat
     ```

4. **Access the UI**
   - Your browser will automatically open to http://localhost:5000
   - If not, manually navigate to http://localhost:5000

### Option 2: Build Windows Executable

1. **Build the executable**
   ```bash
   build.bat
   ```

2. **Run the executable**
   - Navigate to `dist\AMC_AI_Studios\`
   - Double-click `AMC_AI_Studios.exe`

## 🎨 How to Use

### Creating a Production

1. Click **"Create"** in the navigation
2. Fill in your production details:
   - Title
   - Type (Feature Film or TV Show)
   - Rating (G, PG, PG-13, R, TV-MA)
   - Genres
   - Story summary (1-3 paragraphs)
   - Tone and style
3. Click **"Create Movie"**
4. Choose to start the AI pipeline immediately or later

### Monitoring Production

1. Click **"Projects"** to see all your productions
2. Watch the pipeline progress through:
   - Script Generation ✍️
   - Casting 🎭
   - Filming 🎥
   - Post-Production 🎞️
   - Marketing 📣
   - Release 🎉

### Virtual Theater Experience

1. Click **"Theater"** to enter the virtual AMC theater
2. View **"Now Showing"** movies (completed productions)
3. Monitor theater activity:
   - NPCs in lobby
   - NPCs watching movies
   - Theater capacity

## 🏗️ Architecture

### Core Components

```
AMC-AI-STUDIOS-/
├── main.py                 # Application entry point
├── launch.bat             # Windows launcher
├── build.bat              # Executable builder
├── requirements.txt       # Python dependencies
├── src/
│   ├── core/
│   │   ├── config.py      # Configuration management
│   │   └── app.py         # Main application
│   ├── pipelines/
│   │   ├── orchestrator.py        # Pipeline coordination
│   │   ├── script_pipeline.py     # Script generation
│   │   ├── casting_pipeline.py    # Actor casting
│   │   ├── filming_pipeline.py    # Scene filming
│   │   ├── post_production_pipeline.py  # Editing
│   │   └── marketing_pipeline.py  # Marketing materials
│   ├── theater/
│   │   ├── theater_manager.py     # Theater state
│   │   └── npc_ai.py              # NPC behaviors
│   ├── ui/
│   │   ├── server.py              # Flask web server
│   │   ├── templates/             # HTML templates
│   │   └── static/                # CSS/JS assets
│   ├── models/
│   │   └── schema.py              # Data models
│   └── utils/
│       ├── logger.py              # Logging utilities
│       └── ai_client.py           # AI service client
└── data/                          # Generated content
    ├── projects/                  # Project files
    ├── actors/                    # AI actor profiles
    └── assets/                    # Generated assets
```

### AI Pipeline Stages

1. **Script Generation**
   - Character creation
   - Scene breakdown
   - Dialogue writing
   - Hollywood-format screenplay

2. **Casting**
   - AI actor profile generation
   - Persistent identity maintenance
   - Role assignment
   - Chemistry scoring

3. **Filming**
   - Scene-by-scene video generation
   - Camera work and framing
   - Lighting and blocking
   - Multiple takes

4. **Post-Production**
   - Scene assembly
   - Color grading
   - Sound design
   - Music composition
   - VFX integration

5. **Marketing**
   - Poster generation
   - Trailer creation
   - Social media assets
   - Press releases

6. **Release**
   - Theater availability
   - Now showing listing

## 🔧 Configuration

Edit `.env` file to customize:

```env
# AI Services
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Application
DEBUG=False
GPU_ENABLED=True
OFFLINE_MODE=False

# Theater
THEATER_CAPACITY=100
NPC_COUNT=20

# Server
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

## 🎭 AI Actors

AI actors maintain persistent identities across productions:
- Consistent facial features
- Consistent voice
- Career history
- Acting style
- Emotional range

Once created, an actor always looks and sounds the same across all roles.

## 🎬 Supported Genres

- Action
- Comedy
- Drama
- Horror
- Sci-Fi
- Fantasy
- Thriller
- Romance
- Mystery
- Adventure

## 📊 Project Status Tracking

Each project tracks progress through all pipeline stages:
- ⏳ Pending
- 🔄 In Progress
- ✅ Completed
- ❌ Failed

## 🤖 NPC Behaviors

NPCs in the virtual theater:
- Enter the lobby
- Navigate to ticket counter
- Purchase tickets
- Buy concessions
- Walk to screening rooms
- Find and sit in seats
- Watch movies
- React emotionally (laugh, gasp, cry, cheer)
- Leave after the movie

## 🎨 UI Features

- **Cinematic Dark Theme**: AMC-inspired design
- **Real-time Updates**: Live pipeline progress
- **Project Dashboard**: Manage all productions
- **Theater Monitor**: Track NPC activity
- **Responsive Design**: Works on all screen sizes

## 📝 Notes

- First run will create necessary directories
- Projects are saved and persist between sessions
- AI actors are reusable across projects
- The system works in limited mode without API keys
- Generated content is stored in the `data/` directory

## 🔒 Privacy & Security

- All data is stored locally
- No data is sent to external services except AI API calls
- API keys are stored in `.env` (not committed to git)
- Generated content remains on your machine

## 🐛 Troubleshooting

**Application won't start**
- Ensure Python 3.10+ is installed
- Check that all dependencies installed: `pip install -r requirements.txt`

**No AI generation happening**
- Check API keys in `.env` file
- System works in template mode without API keys

**Browser doesn't open**
- Manually navigate to http://localhost:5000

**Port already in use**
- Change FLASK_PORT in `.env` file

## 📜 License

All Rights Reserved © 2024 AMC AI Studios

## 🙏 Acknowledgments

This project demonstrates the future of AI-powered entertainment production, combining multiple AI technologies into a cohesive production pipeline.

---

**Built with ❤️ using AI**