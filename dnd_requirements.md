# D&D AI Dungeon Master Setup Guide (Modular Version)

## Project Structure

The system is now organized into a professional modular structure:

```
dnd_dungeon_master/
├── __init__.py                 # Main package
├── config.py                   # Configuration management
├── models/
│   ├── __init__.py
│   ├── player.py              # Player character and party models
│   └── game_elements.py       # NPC, Quest, Location models
├── data_managers/
│   ├── __init__.py
│   ├── player_data.py         # Player data file management
│   └── game_store.py          # Vector database operations
├── core/
│   ├── __init__.py
│   └── dungeon_master.py      # Main DM logic and LangChain integration
├── examples/
│   ├── __init__.py
│   └── sample_campaign.py     # Sample campaign setup
├── main.py                    # Entry point and game loop
└── requirements.txt           # Dependencies

# Data directories (created at runtime)
player_data/                   # Player character and party files
dnd_vector_db/                 # ChromaDB vector store
```

## Requirements

Create a `requirements.txt` file with the following dependencies:

```
langchain==0.2.16
langchain-openai==0.1.23
langchain-community==0.2.16
langchain-core==0.2.38
langchain-chroma==0.1.4
chromadb==0.4.22
tiktoken==0.7.0
python-dotenv==1.0.0
pydantic==2.8.2
```

## Environment Setup

**Important: Use a Virtual Environment**

To avoid package conflicts, it's highly recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv dnd_dm_env

# Activate virtual environment
# On Windows:
dnd_dm_env\Scripts\activate
# On macOS/Linux:
source dnd_dm_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

1. **Clean Installation (Recommended)**
   
   First, uninstall any existing LangChain packages to avoid conflicts:
   ```bash
   pip uninstall langchain langchain-openai langchain-community langchain-core -y
   ```
   
   Then install the compatible versions:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install langchain==0.2.16 langchain-openai==0.1.23 langchain-community==0.2.16 langchain-core==0.2.38
   pip install chromadb==0.4.22 tiktoken==0.7.0 python-dotenv==1.0.0 pydantic==2.8.2
   ```

2. **Set up OpenRouter API Key**
   
   Get your API key from [OpenRouter](https://openrouter.ai/) and choose one of these methods:

   **Method 1: Create a .env file (Recommended)**
   
   Create a `.env` file in your project directory:
   ```bash
   # .env file
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```
   
   **Method 2: Set environment variable**
   ```bash
   # Linux/Mac
   export OPENROUTER_API_KEY="your_api_key_here"
   
   # Windows Command Prompt
   set OPENROUTER_API_KEY=your_api_key_here
   
   # Windows PowerShell
   $env:OPENROUTER_API_KEY="your_api_key_here"
   ```

3. **Important Security Notes**
   - **Never commit your `.env` file to version control**
   - Add `.env` to your `.gitignore` file:
     ```bash
     echo ".env" >> .gitignore
     ```
   - Keep your API key secure and don't share it publicly

4. **Create Example Files**
   
   Create a `.env.example` file for documentation (safe to commit):
   ```bash
   # .env.example
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
   
   Create a `.gitignore` file to exclude sensitive files:
   ```bash
   # .gitignore
   .env
   __pycache__/
   *.pyc
   dnd_vector_db/
   .DS_Store
   ```

5. **Run the System**
   ```bash
   python dnd_dungeon_master.py
   ```

6. **Quick Start**

   For a completely new setup:
   ```bash
   # Run the setup script to create directory structure
   python setup.py
   
   # Move your Python files to the appropriate directories (see setup output)
   # OR copy the individual files from the artifacts above
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment
   cp .env.example .env
   # Edit .env with your OpenRouter API key
   
   # Run the system
   python main.py
   ```

7. **Advanced Usage**

   ```bash
   # Run with specific party file
   python main.py --party my_custom_party.json
   
   # Enable debug mode
   PYTHONDEBUG=1 python main.py
   
   # Use custom player data directory
   python -c "
   from dnd_dungeon_master import DMConfig, DungeonMaster
   config = DMConfig()
   config.player_data_dir = './my_campaign_data'
   dm = DungeonMaster(config)
   # ... rest of your code
   "
   ```

## System Architecture

### Core Components

1. **DungeonMaster Class** - Main orchestrator that handles:
   - Story generation using LangChain prompts
   - Player interaction and response generation
   - Integration with the vector store for context retrieval

2. **GameElementStore Class** - Manages persistent game data:
   - Vector database storage using ChromaDB
   - NPCs, Quests, and Locations with semantic search
   - Contextual retrieval based on current game situation

3. **Data Models** - Structured data classes for:
   - NPCs (Non-Player Characters)
   - Quests (with objectives, status, rewards)
   - Locations (with connections, features, atmosphere)

### Key Features

- **Semantic Search**: Uses vector embeddings to find relevant NPCs, quests, and locations based on current context
- **Conversation Memory**: Maintains chat history for context-aware responses
- **Persistent Storage**: Game elements are stored in ChromaDB for persistence across sessions
- **Player Data Management**: Loads character sheets and party information from JSON files
- **Modular Design**: Easy to extend with additional game elements or modify behavior
- **Contextual Awareness**: Automatically retrieves relevant game content based on player actions

## Usage Examples

### Adding New Game Elements

```python
# Add a new NPC
dm.add_npc_to_story(
    name="Captain Ironforge",
    description="A grizzled veteran with scars telling tales of countless battles",
    personality="stern but fair, values honor above all",
    location="Town Guard Post",
    role="guard captain",
    relationship="authority figure"
)

# Add a new quest
dm.add_quest_to_story(
    title="Bandit Trouble",
    description="Bandits have been raiding merchant caravans on the eastern road",
    giver="Captain Ironforge",
    objectives=["Investigate bandit camp", "Capture or defeat bandit leader"],
    rewards="100 gold and town's gratitude",
    difficulty="medium",
    location="Eastern Road"
)

# Add a new location
dm.add_location_to_story(
    name="Abandoned Mine",
    description="A dark, echoing mine shaft that was mysteriously abandoned years ago",
    location_type="dungeon",
    features=["collapsed tunnels", "strange echoes", "old mining equipment"],
    atmosphere="eerie and foreboding"
)
```

### Managing Player Data

```python
# Load party from custom file
dm.load_party_from_file("my_campaign_party.json")

# Create new example party and characters
dm.create_example_party()

# Get party information
party_summary = dm.get_party_summary()
print(party_summary)

# Access individual characters
if dm.party:
    for character in dm.party.members:
        print(f"{character.name}: AC {character.armor_class}, HP {character.hit_points}")
        print(f"Stats: {character.stats}")
```

### Game Flow

1. **Initialization**: The system loads existing game data from the vector store and player data from JSON files
2. **Player Data Loading**: Character sheets and party information are loaded from the `./player_data/` directory
3. **Context Retrieval**: For each player action, relevant NPCs, quests, locations, and player information are retrieved
4. **Story Generation**: LangChain prompts combine all context with conversation history to generate responses
5. **Persistence**: New game elements are automatically stored in the vector database

## Configuration Options

### DMConfig Class Settings

- `model_name`: OpenAI model to use (default: "openai/gpt-3.5-turbo")
- `vector_db_path`: Local path for ChromaDB storage
- `openrouter_base_url`: OpenRouter API endpoint

### Prompt Customization

The system prompt can be modified in the `_setup_prompts()` method to change the DM's personality and behavior:

```python
system_template = """You are an expert Dungeon Master with a [specific style]...
- Add custom guidelines
- Modify tone and approach
- Include campaign-specific rules
"""
```

### Memory Management

Adjust conversation memory in the DungeonMaster constructor:

```python
self.memory = ConversationBufferWindowMemory(
    k=20,  # Increase for longer memory
    return_messages=True
)
```

## Production Considerations

1. **Database Scaling**: For large campaigns, consider using a production vector database like Pinecone or Weaviate
2. **Error Handling**: Add comprehensive error handling for API failures and data corruption
3. **Authentication**: Implement user authentication for multi-player campaigns
4. **Backup Strategy**: Regular backups of the vector database and player data for campaign preservation
5. **Rate Limiting**: Implement rate limiting for API calls to avoid exceeding OpenRouter limits
6. **Package Management**: Keep LangChain packages updated as the ecosystem evolves rapidly
   ```bash
   pip install --upgrade langchain langchain-openai langchain-community
   ```

## In-Game Commands

The system supports several special commands during gameplay:

- `quit` or `exit` or `q`: Exit the game
- `party`: Display current party information and stats
- `location`: Show current location
- Any other input: Regular player action that the DM will respond to

## Troubleshooting

### Common Issues

1. **API Key Issues**: 
   - Ensure your OpenRouter API key is valid and has sufficient credits
   - Verify the environment variable is loaded correctly:
     ```python
     import os
     print("API Key loaded:", "Yes" if os.getenv("OPENROUTER_API_KEY") else "No")
     ```
   - Check that your `.env` file is in the same directory as your Python script
   - Make sure there are no extra spaces around the `=` in your `.env` file

2. **Player Data Issues**: 
   - If character files are corrupted, delete the `./player_data/` directory and restart to regenerate examples
   - Check JSON syntax in character files - common issues include missing commas, quotes, or brackets
   - Verify that all character files referenced in `party.json` exist in the player_data directory

3. **Vector Store Errors**: Delete the `./dnd_vector_db` directory to reset the database

4. **Memory Issues**: Reduce the conversation window size if experiencing memory problems

5. **Import Errors**: Ensure all dependencies are installed with correct versions
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Debug Mode

Add debug logging by modifying the main function:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will provide detailed information about API calls and vector store operations.