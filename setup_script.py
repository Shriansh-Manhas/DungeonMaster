#!/usr/bin/env python3
"""
Setup script for D&D AI Dungeon Master
Creates the proper directory structure and initializes the project.
"""

import os
import sys


def create_directory_structure():
    """Create the project directory structure"""
    
    directories = [
        "dnd_dungeon_master",
        "dnd_dungeon_master/models",
        "dnd_dungeon_master/data_managers", 
        "dnd_dungeon_master/core",
        "dnd_dungeon_master/examples",
        "player_data",
        "dnd_vector_db"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


def create_init_files():
    """Create __init__.py files for all packages"""
    
    init_contents = {
        "dnd_dungeon_master/__init__.py": '''"""
D&D AI Dungeon Master

A sophisticated Dungeons & Dragons Dungeon Master powered by LangChain and OpenAI models.
"""

__version__ = "1.0.0"

from .config import DMConfig
from .core.dungeon_master import DungeonMaster

__all__ = ['DMConfig', 'DungeonMaster']
''',
        
        "dnd_dungeon_master/models/__init__.py": '''"""Data models for the D&D Dungeon Master system."""

from .player import PlayerCharacter, Party
from .game_elements import NPC, Quest, Location

__all__ = ['PlayerCharacter', 'Party', 'NPC', 'Quest', 'Location']
''',
        
        "dnd_dungeon_master/data_managers/__init__.py": '''"""Data management classes."""

from .player_data import PlayerDataManager
from .game_store import GameElementStore

__all__ = ['PlayerDataManager', 'GameElementStore']
''',
        
        "dnd_dungeon_master/core/__init__.py": '''"""Core functionality."""

from .dungeon_master import DungeonMaster

__all__ = ['DungeonMaster']
''',
        
        "dnd_dungeon_master/examples/__init__.py": '''"""Example content and setup functions."""

from .sample_campaign import setup_sample_campaign, create_example_party

__all__ = ['setup_sample_campaign', 'create_example_party']
'''
    }
    
    for filepath, content in init_contents.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filepath}")


def create_requirements_file():
    """Create requirements.txt file"""
    
    requirements = """langchain==0.2.16
langchain-openai==0.1.23
langchain-community==0.2.16
langchain-core==0.2.38
langchain-chroma==0.1.4
chromadb==0.4.22
tiktoken==0.7.0
python-dotenv==1.0.0
pydantic==2.8.2
"""
    
    with open("requirements.txt", 'w') as f:
        f.write(requirements)
    print("Created: requirements.txt")


def create_env_example():
    """Create .env.example file"""
    
    env_example = """# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Customize paths (defaults shown)
# VECTOR_DB_PATH=./dnd_vector_db
# PLAYER_DATA_DIR=./player_data
"""
    
    with open(".env.example", 'w') as f:
        f.write(env_example)
    print("Created: .env.example")


def create_gitignore():
    """Create .gitignore file"""
    
    gitignore = """.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.DS_Store
.vscode/
.idea/
*.log
dnd_vector_db/
*.egg-info/
dist/
build/
"""
    
    with open(".gitignore", 'w') as f:
        f.write(gitignore)
    print("Created: .gitignore")


def main():
    """Main setup function"""
    
    print("Setting up D&D AI Dungeon Master Project Structure")
    print("=" * 60)
    
    try:
        # Create directory structure
        print("\nCreating directories...")
        create_directory_structure()
        
        # Create __init__.py files
        print("\nCreating package files...")
        create_init_files()
        
        # Create requirements.txt
        print("\nCreating requirements file...")
        create_requirements_file()
        
        # Create .env.example
        print("\nCreating configuration examples...")
        create_env_example()
        
        # Create .gitignore
        print("\nCreating .gitignore...")
        create_gitignore()
        
        print("\n" + "=" * 60)
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("1. Copy your individual Python files into the appropriate directories:")
        print("   - config.py -> dnd_dungeon_master/")
        print("   - player.py -> dnd_dungeon_master/models/")
        print("   - game_elements.py -> dnd_dungeon_master/models/")
        print("   - player_data.py -> dnd_dungeon_master/data_managers/")
        print("   - game_store.py -> dnd_dungeon_master/data_managers/")
        print("   - dungeon_master.py -> dnd_dungeon_master/core/")
        print("   - sample_campaign.py -> dnd_dungeon_master/examples/")
        print("   - main.py -> project root")
        print()
        print("2. Install dependencies:")
        print("   pip install -r requirements.txt")
        print()
        print("3. Set up your API key:")
        print("   cp .env.example .env")
        print("   # Edit .env with your actual OpenRouter API key")
        print()
        print("4. Run the system:")
        print("   python main.py")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()