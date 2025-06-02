"""
D&D AI Dungeon Master - Main Entry Point

A sophisticated D&D Dungeon Master powered by LangChain and OpenAI models,
with persistent character and world data storage.
"""

import sys
import os

# Add the project root to the Python path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from dnd_dungeon_master.config import DMConfig
from dnd_dungeon_master.core.dungeon_master import DungeonMaster
from dnd_dungeon_master.examples.sample_campaign import (
    setup_initial_campaign_state, 
    get_campaign_intro
)


def print_welcome():
    """Print welcome message and basic instructions"""
    print("=" * 60)
    print("Welcome to the AI Dungeon Master!")
    print("=" * 60)
    print()
    print("Commands:")
    print("  'quit', 'exit', or 'q' - Exit the game")
    print("  'party' - Show party information")
    print("  'location' - Show current location")
    print("  'context' - Show current game context")
    print("  'help' - Show this help message")
    print("  Any other input - Player action for the DM to respond to")
    print()


def print_help():
    """Print help information"""
    print("\n" + "=" * 40)
    print("HELP - How to Play")
    print("=" * 40)
    print()
    print("Basic Commands:")
    print("  party     - View detailed party information")
    print("  location  - See where you currently are")
    print("  context   - Get current game state summary")
    print("  help      - Show this help message")
    print("  quit      - Exit the game")
    print()
    print("Playing the Game:")
    print("  - Type any action or dialogue for your party")
    print("  - The DM will respond and advance the story")
    print("  - Be descriptive! 'I search the room' vs 'I carefully examine the ancient bookshelf'")
    print("  - The DM knows your characters' abilities and will ask for dice rolls when needed")
    print()
    print("Example Actions:")
    print("  'We approach the barkeeper and ask about local rumors'")
    print("  'Thorin examines the tracks while Pip searches for traps'")
    print("  'Elaria casts Detect Magic to scan the area'")
    print("  'We rest for the night and discuss our plans'")
    print()


def handle_special_commands(user_input: str, dm: DungeonMaster) -> bool:
    """
    Handle special commands that don't require DM response.
    Returns True if a special command was handled, False otherwise.
    """
    command = user_input.lower().strip()
    
    if command in ['quit', 'exit', 'q']:
        print("\nThanks for playing! May your dice always roll high!")
        return True
    
    elif command == 'party':
        print("\n" + "=" * 40)
        print("PARTY INFORMATION")
        print("=" * 40)
        print(dm.get_party_summary())
        print()
        return False
    
    elif command == 'location':
        print(f"\nCurrent Location: {dm.current_location}")
        if dm.current_location:
            # Try to get location details
            locations = dm.game_store.search_elements(dm.current_location, 'location', k=1)
            if locations:
                loc = locations[0]
                print(f"Description: {loc['description']}")
                print(f"Type: {loc['type'].title()}")
                print(f"Atmosphere: {loc['atmosphere']}")
        print()
        return False
    
    elif command == 'context':
        print("\n" + "=" * 40)
        print("CURRENT GAME CONTEXT")
        print("=" * 40)
        print(dm.get_current_context_summary())
        print()
        return False
    
    elif command == 'help':
        print_help()
        return False
    
    return False


def main():
    """Main function to run the DM system"""
    
    try:
        # Initialize configuration
        print("Initializing D&D Dungeon Master...")
        config = DMConfig()
        config.validate_directories()
        
        # Create DM instance
        dm = DungeonMaster(config)
        
        # Setup initial campaign state
        setup_initial_campaign_state(dm)
        
        # Print welcome and initial setup
        print_welcome()
        
        # Show party info
        print("PARTY STATUS:")
        print(dm.get_party_summary())
        print()
        
        # Show campaign intro
        print("CAMPAIGN INTRODUCTION:")
        print(get_campaign_intro())
        
        # Initial scene setting
        print("THE STORY BEGINS...")
        initial_response = dm.generate_response(
            "The party enters the Riverside Tavern for the first time, looking around and taking in the atmosphere. "
            "They're new to the area and interested in learning about local opportunities for adventure."
        )
        print(f"DM: {initial_response}\n")
        
        # Main game loop
        while True:
            try:
                user_input = input("Player Action: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                should_quit = handle_special_commands(user_input, dm)
                if should_quit:
                    break
                
                # Skip if special command was handled (but don't quit)
                if user_input.lower() in ['party', 'location', 'context', 'help']:
                    continue
                
                # Generate DM response for regular actions
                print("\nDM Response:")
                dm_response = dm.generate_response(user_input)
                print(f"DM: {dm_response}\n")
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("The DM needs a moment to collect their thoughts...\n")
                
                # If it's a critical error, we might want to exit
                if "API" in str(e) or "connection" in str(e).lower():
                    print("This appears to be a connection issue. Please check your API key and internet connection.")
                    retry = input("Would you like to try again? (y/n): ").strip().lower()
                    if retry != 'y':
                        break
    
    except Exception as e:
        print(f"\nFailed to initialize the Dungeon Master: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your OPENROUTER_API_KEY is set correctly")
        print("2. Check that all required packages are installed: pip install -r requirements.txt")
        print("3. Ensure you have a stable internet connection")
        sys.exit(1)


if __name__ == "__main__":
    main()