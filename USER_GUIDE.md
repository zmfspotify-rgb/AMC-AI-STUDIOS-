# AMC AI Studios - User Guide

Welcome to AMC AI Studios! This guide will help you create your first AI-generated movie or TV show.

## Getting Started

### First-Time Setup

1. **Download and Extract**
   - Download AMC AI Studios
   - Extract to a folder on your computer

2. **Launch the Application**
   - Find `launch.bat` in the application folder
   - Double-click `launch.bat`
   - Wait for the application to start (first launch may take longer)
   - Your web browser will automatically open

3. **Optional: Add AI API Keys**
   - For enhanced AI features, you can add API keys
   - Open `.env` file in a text editor
   - Add your OpenAI or Anthropic API key
   - Restart the application

## Creating Your First Movie

### Step 1: Access the Create Page

1. The application opens to the **Create** page
2. If not, click the **Create** button in the navigation

### Step 2: Fill in Project Details

**Title**
- Enter your movie or TV show title
- Example: "The Last Horizon"

**Type**
- Choose **Feature Film** for a movie
- Choose **TV Show** for a series

**Rating**
- Select appropriate content rating:
  - **G**: General Audiences
  - **PG**: Parental Guidance
  - **PG-13**: Parents Strongly Cautioned
  - **R**: Restricted
  - **TV-MA**: Mature Audiences Only

**Runtime (for Films)**
- Set movie length in minutes
- Typical range: 90-150 minutes

**Seasons & Episodes (for TV Shows)**
- Number of seasons
- Episodes per season

**Genres**
- Select one or more genres
- Hold Ctrl/Cmd to select multiple
- Options: Action, Comedy, Drama, Horror, Sci-Fi, Fantasy, Thriller, Romance, Mystery, Adventure

**Tone**
- Choose the overall feel:
  - **Light**: Fun and uplifting
  - **Balanced**: Mix of light and serious
  - **Dark**: Serious and intense
  - **Gritty**: Raw and realistic
  - **Hopeful**: Inspiring
  - **Cinematic**: Epic and grand

**Story Summary**
- Write 1-3 paragraphs describing your story
- Include:
  - Main character(s)
  - Central conflict
  - Setting
  - Key events

### Step 3: Create the Project

1. Click the **🎬 Create Movie** button
2. Confirm you want to start the AI pipeline
3. Watch the magic happen!

## Understanding the Production Pipeline

Your project goes through six stages:

### 1. Script Generation ✍️
- AI creates characters
- Develops scene-by-scene outline
- Writes dialogue
- Formats in Hollywood screenplay style

**What happens:**
- Character profiles are created
- Scene breakdown is generated
- Dialogue is written
- Action descriptions are added

### 2. Casting 🎭
- AI actors are assigned to characters
- Each actor has a unique identity
- Actors are persistent and reusable

**What you get:**
- Named AI actors
- Consistent appearances
- Character-actor pairings

### 3. Filming 🎥
- Scenes are "filmed"
- Camera angles determined
- Lighting and blocking planned
- Multiple takes generated

**Output:**
- Scene-by-scene video metadata
- Camera specifications
- Lighting plans

### 4. Post-Production 🎞️
- Scenes assembled in order
- Color grading applied
- Sound design added
- Music composed
- Visual effects integrated

**Final touches:**
- Professional color grading
- Spatial audio mix
- Original musical score
- Polished final cut

### 5. Marketing 📣
- Posters created
- Trailers generated
- Social media assets prepared
- Press releases written

**Promotional materials:**
- Movie poster
- Multiple trailer versions
- Social media posts
- Press kit

### 6. Release 🎉
- Project marked as complete
- Added to theater "Now Showing"
- Ready for viewing

## Viewing Your Projects

### Projects Page

1. Click **Projects** in the navigation
2. See all your productions
3. Each project card shows:
   - Title
   - Type (Film or TV)
   - Creation date
   - Status of each pipeline stage

### Status Indicators

- **⏳ Pending**: Not started yet
- **🔄 In Progress**: Currently processing
- **✅ Completed**: Successfully finished
- **❌ Failed**: Encountered an error

## Virtual AMC Theater

### Accessing the Theater

1. Click **Theater** in the navigation
2. Explore the virtual cinema experience

### Now Showing

- Lists all completed movies
- Shows title, rating, genres, and runtime
- Click to view details

### Theater Statistics

Monitor the virtual theater activity:

- **NPCs Present**: Total number of AI moviegoers
- **In Lobby**: NPCs in the lobby area
- **Watching Movies**: NPCs currently in theaters

### About the NPCs

The virtual theater features AI-driven Non-Player Characters (NPCs) that:

- **Navigate**: Walk through lobby, hallways, and theaters
- **Purchase**: Buy tickets and concessions
- **Watch**: Sit in theaters and watch movies
- **React**: Laugh, gasp, clap, and respond to scenes
- **Socialize**: Interact with the environment

NPCs make autonomous decisions and create a living, breathing theater environment!

## Tips for Best Results

### Writing Story Summaries

**Good Example:**
```
In a dystopian future, a young hacker named Maya discovers 
she can manipulate the city's AI control system. When she 
uncovers a conspiracy to erase human memories, she must team 
up with a rogue android to save humanity's collective 
consciousness. Racing against time, they navigate virtual 
worlds and physical danger to restore freedom to the city.
```

**Include:**
- Main character(s) and their role
- The central problem or conflict
- The setting (time and place)
- Stakes (what's at risk)
- Brief arc (beginning, middle, end)

### Choosing Genres

- Be specific but not too narrow
- 1-3 genres work best
- Mix complementary genres (Action + Sci-Fi)
- Avoid contradictory combinations

### Setting Runtime

- **Short films**: 60-80 minutes
- **Standard films**: 90-120 minutes
- **Epic films**: 120-180 minutes
- **TV episodes**: 20-60 minutes per episode

## Troubleshooting

### Application Won't Start

**Problem**: Double-clicking launch.bat does nothing

**Solutions:**
- Check if Python is installed
- Right-click launch.bat → "Run as Administrator"
- Check antivirus isn't blocking the application

### Browser Doesn't Open

**Problem**: Application starts but browser doesn't open

**Solution:**
- Manually open your web browser
- Navigate to: http://localhost:5000

### Pipeline Stuck

**Problem**: Project is stuck "In Progress"

**Solutions:**
- Wait - AI processing takes time (5-15 minutes)
- Refresh the Projects page
- Check the console window for errors
- Restart the application

### No AI Generation

**Problem**: Projects create but content is basic/template

**Explanation:**
- This is normal without API keys
- System works in "template mode"
- To enable full AI:
  - Add OpenAI or Anthropic API key to `.env`
  - Restart application

## Keyboard Shortcuts

- **Browser only** (standard browser shortcuts apply)
- **Refresh page**: F5
- **Close application**: Close the console window or press Ctrl+C in console

## Best Practices

1. **Start Simple**: Create a short film first to learn the system
2. **Iterate**: Review results and create new versions
3. **Experiment**: Try different genres, tones, and styles
4. **Be Detailed**: More detailed story summaries yield better results
5. **Monitor Progress**: Watch the pipeline stages to understand the process

## FAQs

**Q: How long does it take to create a movie?**
A: 5-15 minutes depending on complexity and AI services used

**Q: Can I edit the script after creation?**
A: Currently, scripts are auto-generated. Future versions may add editing

**Q: Are my projects saved?**
A: Yes! All projects persist in the `data/projects` folder

**Q: Can I create multiple projects?**
A: Absolutely! Create as many as you like

**Q: Do I need internet?**
A: For template mode, no. For full AI features, yes (for API calls)

**Q: Is my data private?**
A: Yes! Everything is stored locally except AI API calls

**Q: Can I share my movies?**
A: Projects are stored as data files. Export features may come in future updates

## Getting Help

If you encounter issues:

1. Check this User Guide
2. Review the console window for error messages
3. Check `logs/` folder for detailed logs
4. Consult the Developer Guide for technical details

## Updates and Version Information

Current Version: 1.0.0

Check the README.md file for:
- Version history
- New features
- Known issues
- Planned enhancements

---

**Enjoy creating your AI-powered entertainment!** 🎬🍿
