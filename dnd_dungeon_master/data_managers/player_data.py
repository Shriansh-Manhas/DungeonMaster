import os
import json
import uuid
from typing import List
from dataclasses import asdict

from ..models import PlayerCharacter, Party


class PlayerDataManager:
    """Manages loading and saving player character data from files"""
    
    def __init__(self, player_data_dir: str = "./player_data"):
        self.player_data_dir = player_data_dir
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Create player data directory if it doesn't exist"""
        os.makedirs(self.player_data_dir, exist_ok=True)
        
    def load_character(self, filename: str) -> PlayerCharacter:
        """Load a character from a JSON file"""
        filepath = os.path.join(self.player_data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return PlayerCharacter(**data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Character file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in character file {filepath}: {e}")
        except TypeError as e:
            raise ValueError(f"Invalid character data structure in {filepath}: {e}")
    
    def save_character(self, character: PlayerCharacter, filename: str = None):
        """Save a character to a JSON file"""
        if filename is None:
            filename = f"{character.name.lower().replace(' ', '_')}.json"
        
        filepath = os.path.join(self.player_data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(asdict(character), file, indent=2, ensure_ascii=False)
    
    def load_party(self, filename: str = "party.json") -> Party:
        """Load party data from a JSON file"""
        filepath = os.path.join(self.player_data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Load individual characters
                members = []
                for member_file in data.get('member_files', []):
                    character = self.load_character(member_file)
                    members.append(character)
                
                # Create party object with loaded members
                party_data = data.copy()
                party_data['members'] = members
                if 'member_files' in party_data:
                    del party_data['member_files']
                
                return Party(**party_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Party file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in party file {filepath}: {e}")
    
    def save_party(self, party: Party, filename: str = "party.json"):
        """Save party data to a JSON file"""
        filepath = os.path.join(self.player_data_dir, filename)
        
        # Save individual characters first
        member_files = []
        for member in party.members:
            char_filename = f"{member.name.lower().replace(' ', '_')}.json"
            self.save_character(member, char_filename)
            member_files.append(char_filename)
        
        # Save party data with references to character files
        party_data = asdict(party)
        party_data['member_files'] = member_files
        del party_data['members']  # Don't duplicate character data
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(party_data, file, indent=2, ensure_ascii=False)
    
    def list_characters(self) -> List[str]:
        """List all available character files"""
        if not os.path.exists(self.player_data_dir):
            return []
        
        files = [f for f in os.listdir(self.player_data_dir) 
                if f.endswith('.json') and f != 'party.json']
        return files
    
    def character_exists(self, filename: str) -> bool:
        """Check if a character file exists"""
        filepath = os.path.join(self.player_data_dir, filename)
        return os.path.exists(filepath)
    
    def party_exists(self, filename: str = "party.json") -> bool:
        """Check if a party file exists"""
        filepath = os.path.join(self.player_data_dir, filename)
        return os.path.exists(filepath)
    
    def delete_character(self, filename: str):
        """Delete a character file"""
        filepath = os.path.join(self.player_data_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    def create_example_character(self, name: str = "example_character") -> str:
        """Create an example character file for reference"""
        example_character = PlayerCharacter(
            id=str(uuid.uuid4()),
            name="Thorin Ironforge",
            character_class="Fighter",
            level=3,
            race="Dwarf",
            background="Soldier",
            alignment="Lawful Good",
            stats={
                "STR": 16,
                "DEX": 12,
                "CON": 15,
                "INT": 10,
                "WIS": 14,
                "CHA": 8
            },
            skills=["Athletics", "Intimidation", "Perception", "Survival"],
            equipment=[
                "Chain Mail",
                "Shield",
                "Warhammer",
                "Handaxe (2)",
                "Explorers Pack",
                "Military Rank Insignia"
            ],
            backstory="A veteran soldier who served in the King's Guard for over a decade.",
            personality_traits=[
                "I face problems head-on with direct, simple solutions",
                "I enjoy being strong and like breaking things"
            ],
            ideals="Responsibility. I do what I must and obey just authority.",
            bonds="My honor is my life. I would rather die than compromise my principles.",
            flaws="I have little respect for anyone who is not a proven warrior.",
            hit_points=29,
            armor_class=18
        )
        
        filename = f"{name}.json"
        self.save_character(example_character, filename)
        return filename
    
    def validate_character_data(self, data: dict) -> bool:
        """Validate character data structure"""
        required_fields = [
            'name', 'character_class', 'level', 'race', 'background',
            'alignment', 'stats', 'skills', 'equipment', 'backstory',
            'personality_traits', 'ideals', 'bonds', 'flaws',
            'hit_points', 'armor_class'
        ]
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate stats structure
        required_stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        if not isinstance(data['stats'], dict):
            return False
        
        for stat in required_stats:
            if stat not in data['stats']:
                return False
        
        return True