#!/usr/bin/env python3
"""
Simple test script to validate AMC AI Studios core functionality
"""

import sys
sys.path.insert(0, '.')

from src.core.config import Config
from src.models.schema import Project, ProjectType, Genre, Rating
from src.pipelines.orchestrator import PipelineOrchestrator
from src.theater.theater_manager import TheaterManager

def test_config():
    """Test configuration loading."""
    print("Testing Configuration...")
    config = Config()
    config.ensure_directories()
    print(f"  ✓ App Name: {config.app_name}")
    print(f"  ✓ Data Dir: {config.data_dir}")
    print(f"  ✓ Theater Capacity: {config.theater_capacity}")
    print(f"  ✓ NPC Count: {config.npc_count}")
    return config

def test_project_creation(orchestrator):
    """Test project creation."""
    print("\nTesting Project Creation...")
    
    project = orchestrator.create_project(
        title="Test Movie",
        story_summary="A test story about testing the AMC AI Studios system.",
        project_type=ProjectType.FEATURE_FILM,
        genres=[Genre.ACTION, Genre.SCIFI],
        rating=Rating.PG13,
        runtime_minutes=90,
        tone="cinematic"
    )
    
    print(f"  ✓ Project created: {project.title}")
    print(f"  ✓ Project ID: {project.id}")
    print(f"  ✓ Type: {project.project_type}")
    print(f"  ✓ Genres: {', '.join(project.genres)}")
    
    return project

def test_script_generation(orchestrator, project):
    """Test script generation."""
    print("\nTesting Script Generation...")
    
    from src.pipelines.script_pipeline import ScriptPipeline
    pipeline = ScriptPipeline(orchestrator.config)
    
    script = pipeline.generate_script(project)
    
    print(f"  ✓ Script created: {script.title}")
    print(f"  ✓ Characters: {len(script.characters)}")
    print(f"  ✓ Scenes: {len(script.scenes)}")
    if script.characters:
        print(f"  ✓ First character: {script.characters[0].name}")
    
    return script

def test_theater(config):
    """Test theater manager."""
    print("\nTesting Theater Manager...")
    
    theater = TheaterManager(config)
    
    print(f"  ✓ NPCs created: {len(theater.npcs)}")
    print(f"  ✓ Locations: {len(theater.locations)}")
    
    # Update theater a few times
    for i in range(3):
        theater.update(1.0)
    
    state = theater.get_theater_state()
    print(f"  ✓ Theater state retrieved")
    
    return theater

def main():
    """Run all tests."""
    print("=" * 60)
    print("AMC AI STUDIOS - System Test")
    print("=" * 60)
    
    try:
        # Test 1: Configuration
        config = test_config()
        
        # Test 2: Orchestrator
        print("\nTesting Pipeline Orchestrator...")
        orchestrator = PipelineOrchestrator(config)
        print(f"  ✓ Orchestrator initialized")
        
        # Test 3: Project Creation
        project = test_project_creation(orchestrator)
        
        # Test 4: Script Generation
        script = test_script_generation(orchestrator, project)
        
        # Test 5: Theater
        theater = test_theater(config)
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nSystem is ready to use!")
        print("Run 'python main.py' to start the full application.")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
