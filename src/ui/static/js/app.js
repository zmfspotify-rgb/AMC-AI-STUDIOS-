// AMC AI Studios - Frontend JavaScript

// Section navigation
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active from all nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(`${sectionName}-section`);
    if (section) {
        section.classList.add('active');
    }
    
    // Activate nav button
    event.target.classList.add('active');
    
    // Load data for section
    if (sectionName === 'projects') {
        loadProjects();
    } else if (sectionName === 'theater') {
        loadTheater();
    }
}

// Toggle project type options
function toggleProjectType() {
    const projectType = document.getElementById('project_type').value;
    const filmOptions = document.getElementById('film-options');
    const tvOptions = document.getElementById('tv-options');
    
    if (projectType === 'feature_film') {
        filmOptions.style.display = 'block';
        tvOptions.style.display = 'none';
    } else {
        filmOptions.style.display = 'none';
        tvOptions.style.display = 'block';
    }
}

// Create project form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const data = {
            title: formData.get('title'),
            project_type: formData.get('project_type'),
            rating: formData.get('rating'),
            story_summary: formData.get('story_summary'),
            tone: formData.get('tone'),
            genres: Array.from(document.getElementById('genres').selectedOptions).map(o => o.value)
        };
        
        // Add type-specific data
        if (data.project_type === 'feature_film') {
            data.runtime_minutes = parseInt(formData.get('runtime_minutes'));
        } else {
            data.num_seasons = parseInt(formData.get('num_seasons'));
            data.num_episodes = parseInt(formData.get('num_episodes'));
        }
        
        try {
            // Show loading
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = '🎬 Creating...';
            submitBtn.disabled = true;
            
            // Create project
            const response = await fetch('/api/projects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showMessage('success', 'Project created successfully!');
                
                // Ask to run pipeline
                if (confirm('Project created! Start the AI production pipeline now?')) {
                    await runPipeline(result.project_id);
                }
                
                // Reset form
                form.reset();
                
                // Switch to projects view
                setTimeout(() => {
                    showSection('projects');
                }, 2000);
            } else {
                showMessage('error', result.error || 'Failed to create project');
            }
            
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            
        } catch (error) {
            console.error('Error:', error);
            showMessage('error', 'Failed to create project');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
    
    // Load projects on page load
    loadProjects();
});

// Run pipeline for a project
async function runPipeline(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}/run`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('success', 'AI production pipeline started! This may take several minutes.');
            
            // Start polling for updates
            pollProjectStatus(projectId);
        } else {
            showMessage('error', 'Failed to start pipeline');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('error', 'Failed to start pipeline');
    }
}

// Poll project status
function pollProjectStatus(projectId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`/api/projects/${projectId}`);
            const project = await response.json();
            
            // Check if all stages are complete
            const allComplete = Object.values(project.status).every(
                status => status === 'completed'
            );
            
            if (allComplete) {
                clearInterval(interval);
                showMessage('success', 'Production complete!');
                loadProjects();
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 5000); // Poll every 5 seconds
}

// Load projects list
async function loadProjects() {
    const container = document.getElementById('projects-list');
    
    try {
        const response = await fetch('/api/projects');
        const projects = await response.json();
        
        if (projects.length === 0) {
            container.innerHTML = '<p class="loading">No projects yet. Create your first production!</p>';
            return;
        }
        
        container.innerHTML = projects.map(project => `
            <div class="project-card">
                <h3 class="project-title">${project.title}</h3>
                <div class="project-meta">
                    ${project.type} • Created ${new Date(project.created_at).toLocaleDateString()}
                </div>
                <div class="project-status">
                    ${Object.entries(project.status).map(([stage, status]) => `
                        <div class="status-item">
                            <span>${formatStageName(stage)}</span>
                            <span class="status-badge status-${status}">${status.replace('_', ' ')}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading projects:', error);
        container.innerHTML = '<p class="message error">Failed to load projects</p>';
    }
}

// Load theater data
async function loadTheater() {
    try {
        // Load now showing
        const showingResponse = await fetch('/api/theater/now-showing');
        const movies = await showingResponse.json();
        
        const showingContainer = document.getElementById('now-showing-list');
        
        if (movies.length === 0) {
            showingContainer.innerHTML = '<p class="loading">No movies available yet. Complete a project first!</p>';
        } else {
            showingContainer.innerHTML = movies.map(movie => `
                <div class="movie-card">
                    <h4 class="movie-title">${movie.title}</h4>
                    <div class="movie-info">
                        ${movie.rating} • ${movie.genres.join(', ')} • ${movie.runtime} min
                    </div>
                </div>
            `).join('');
        }
        
        // Load theater state
        const stateResponse = await fetch('/api/theater/state');
        const state = await stateResponse.json();
        
        document.getElementById('npc-count').textContent = state.npcs.length;
        
        // Count NPCs in different areas
        const inLobby = state.npcs.filter(npc => 
            npc.current_action.includes('lobby')
        ).length;
        
        const watching = state.npcs.filter(npc => 
            npc.current_action === 'watching_movie'
        ).length;
        
        document.getElementById('lobby-count').textContent = inLobby;
        document.getElementById('watching-count').textContent = watching;
        
    } catch (error) {
        console.error('Error loading theater:', error);
    }
}

// Show message
function showMessage(type, text) {
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    
    // Insert at top of main content
    const main = document.querySelector('.app-main');
    main.insertBefore(message, main.firstChild);
    
    // Remove after 5 seconds
    setTimeout(() => {
        message.remove();
    }, 5000);
}

// Format stage names
function formatStageName(stage) {
    return stage.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

// Auto-refresh theater state every 10 seconds
setInterval(() => {
    const theaterSection = document.getElementById('theater-section');
    if (theaterSection && theaterSection.classList.contains('active')) {
        loadTheater();
    }
}, 10000);
