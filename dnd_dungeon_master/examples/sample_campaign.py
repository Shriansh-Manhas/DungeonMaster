import uuid
import json
import os
from dataclasses import asdict

from ..models import PlayerCharacter, Party
from ..core.dungeon_master import DungeonMaster


def setup_sample_campaign(dm: DungeonMaster):
    """Setup a sample campaign with some initial content"""
    
    # Add some sample locations
    dm.add_location_to_story(
        name="Riverside Tavern",
        description="A cozy tavern by the river, filled with the warm glow of firelight and the sound of laughter.",
        location_type="building",
        features=["comfortable seating", "excellent ale", "local rumors", "traveling merchants"],
        atmosphere="welcoming and lively"
    )
    
    dm.add_location_to_story(
        name="Whispering Woods",
        description="A dense forest where ancient trees tower overhead and mysterious sounds echo through the undergrowth.",
        location_type="wilderness",
        features=["ancient ruins", "mysterious fog", "hidden paths", "magical creatures"],
        connected_locations=["Riverside Village", "Old Mine Entrance"],
        atmosphere="mysterious and slightly ominous"
    )
    
    dm.add_location_to_story(
        name="Riverside Village",
        description="A peaceful farming village built along the banks of a gentle river.",
        location_type="town",
        features=["market square", "stone bridge", "watermills", "village shrine"],
        connected_locations=["Whispering Woods", "Eastern Road"],
        atmosphere="peaceful and rustic"
    )
    
    # Add some sample NPCs
    dm.add_npc_to_story(
        name="Gareth the Barkeeper",
        description="A burly dwarf with a braided beard and kind eyes, always ready with a story or a drink.",
        personality="friendly, talkative, knows everyone's business",
        location="Riverside Tavern",
        role="tavern keeper and information broker",
        relationship="friendly",
        dialogue_style="casual and warm"
    )
    
    dm.add_npc_to_story(
        name="Elara Moonwhisper",
        description="A mysterious elven ranger with silver hair and piercing green eyes, often seen at the forest's edge.",
        personality="cautious, wise, protective of nature",
        location="Whispering Woods",
        role="forest guardian and guide",
        relationship="neutral",
        dialogue_style="formal and measured"
    )
    
    dm.add_npc_to_story(
        name="Mayor Aldric Brightwater",
        description="A middle-aged human with graying hair and worry lines, clearly burdened by his responsibilities.",
        personality="responsible, worried, seeks solutions to village problems",
        location="Riverside Village",
        role="village leader and quest giver",
        relationship="respectful",
        dialogue_style="formal but earnest"
    )
    
    # Add some sample quests
    dm.add_quest_to_story(
        title="The Missing Merchant",
        description="A merchant caravan has failed to arrive in town, and their route passes through the Whispering Woods.",
        giver="Gareth the Barkeeper",
        objectives=["Investigate the merchant's route", "Find signs of what happened", "Rescue survivors if any"],
        rewards="50 gold pieces and the merchant's gratitude",
        difficulty="easy",
        location="Whispering Woods"
    )
    
    dm.add_quest_to_story(
        title="Strange Lights in the Forest",
        description="Villagers have reported strange, dancing lights deep in the Whispering Woods at night.",
        giver="Mayor Aldric Brightwater",
        objectives=["Investigate the source of the lights", "Determine if they pose a threat", "Report back to the mayor"],
        rewards="75 gold pieces and village gratitude",
        difficulty="medium",
        location="Whispering Woods"
    )
    
    dm.add_quest_to_story(
        title="Goblin Raids",
        description="Goblins have been raiding farms on the outskirts of the village, stealing livestock and crops.",
        giver="Mayor Aldric Brightwater",
        objectives=["Find the goblin camp", "Stop the raids", "Recover stolen goods if possible"],
        rewards="100 gold pieces and improved village reputation",
        difficulty="medium",
        location="Eastern Road"
    )


def create_example_party(player_data_dir: str = "./player_data"):
    """Create example party and character files"""
    print("Creating example party and characters...")
    
    # Ensure directory exists
    os.makedirs(player_data_dir, exist_ok=True)
    
    # Create example characters
    characters = []
    character_files = []
    
    # Fighter - Thorin Ironforge
    thorin = PlayerCharacter(
        id=str(uuid.uuid4()),
        name="Thorin Ironforge",
        character_class="Fighter",
        level=2,
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
            "Explorer's Pack",
            "Military Rank Insignia"
        ],
        backstory="A veteran soldier who served in the King's Guard. Left after witnessing corruption, now seeks honor as an adventurer.",
        personality_traits=[
            "I face problems head-on with direct solutions",
            "I enjoy displays of strength and breaking things"
        ],
        ideals="Responsibility. I do what I must and obey just authority.",
        bonds="My honor is my life. I would rather die than compromise my principles.",
        flaws="I have little respect for anyone who is not a proven warrior.",
        hit_points=20,
        armor_class=18
    )
    
    # Wizard - Elaria Starweaver
    elaria = PlayerCharacter(
        id=str(uuid.uuid4()),
        name="Elaria Starweaver",
        character_class="Wizard",
        level=2,
        race="Elf",
        background="Sage",
        alignment="Neutral Good",
        stats={
            "STR": 8,
            "DEX": 14,
            "CON": 13,
            "INT": 16,
            "WIS": 12,
            "CHA": 11
        },
        skills=["Arcana", "History", "Investigation", "Medicine"],
        equipment=[
            "Spellbook",
            "Quarterstaff",
            "Dagger",
            "Component Pouch",
            "Scholar's Pack",
            "Ink and Quill",
            "Spell Scroll (Magic Missile)"
        ],
        backstory="A young elf who spent decades studying ancient magic in great libraries. Seeks practical experience to complement theoretical knowledge.",
        personality_traits=[
            "I am awkward in social situations",
            "I speak without thinking, sometimes insulting others"
        ],
        ideals="Knowledge. The path to power and improvement is through understanding.",
        bonds="The library where I learned is the most important place to me.",
        flaws="I overlook obvious solutions in favor of complicated ones.",
        hit_points=14,
        armor_class=12
    )
    
    # Rogue - Pip Lightfingers
    pip = PlayerCharacter(
        id=str(uuid.uuid4()),
        name="Pip Lightfingers",
        character_class="Rogue",
        level=2,
        race="Halfling",
        background="Criminal",
        alignment="Chaotic Good",
        stats={
            "STR": 10,
            "DEX": 16,
            "CON": 14,
            "INT": 12,
            "WIS": 13,
            "CHA": 15
        },
        skills=["Stealth", "Sleight of Hand", "Investigation", "Deception", "Insight", "Perception"],
        equipment=[
            "Leather Armor",
            "Shortsword",
            "Shortbow",
            "Thieves' Tools",
            "Burglar's Pack",
            "Crowbar",
            "Dark Cloak"
        ],
        backstory="A former street thief who turned to adventuring after helping the wrong person escape from the law.",
        personality_traits=[
            "I always have a plan for what to do when things go wrong",
            "I am incredibly slow to trust, but those who prove themselves earn my loyalty"
        ],
        ideals="Redemption. Everyone deserves a second chance.",
        bonds="I'm trying to pay back a debt I owe to my generous benefactor.",
        flaws="When I see something valuable, I can't think about anything but how to steal it.",
        hit_points=16,
        armor_class=13
    )
    
    # Cleric - Brother Marcus
    marcus = PlayerCharacter(
        id=str(uuid.uuid4()),
        name="Brother Marcus",
        character_class="Cleric",
        level=2,
        race="Human",
        background="Acolyte",
        alignment="Lawful Good",
        stats={
            "STR": 14,
            "DEX": 10,
            "CON": 15,
            "INT": 12,
            "WIS": 16,
            "CHA": 13
        },
        skills=["Medicine", "Religion", "Insight", "Persuasion"],
        equipment=[
            "Chain Shirt",
            "Shield",
            "Mace",
            "Light Crossbow",
            "Priest's Pack",
            "Holy Symbol",
            "Prayer Book"
        ],
        backstory="A devoted priest who left his temple to spread healing and hope in the wider world.",
        personality_traits=[
            "I see omens in every event and action",
            "I quote sacred texts in almost every situation"
        ],
        ideals="Faith. I trust that my deity will guide my actions.",
        bonds="I would die to recover an ancient relic of my faith that was lost long ago.",
        flaws="I judge others harshly, and myself even more severely.",
        hit_points=18,
        armor_class=16
    )
    
    characters = [thorin, elaria, pip, marcus]
    
    # Save character files
    for character in characters:
        filename = f"{character.name.lower().replace(' ', '_')}.json"
        filepath = os.path.join(player_data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(character), f, indent=2, ensure_ascii=False)
        
        character_files.append(filename)
    
    # Create party
    party = Party(
        name="The Brave Companions",
        members=[],  # Will be loaded from files
        formation="Thorin takes point, Elaria and Marcus in the middle, Pip scouts ahead or brings up the rear",
        shared_equipment=[
            "Rope (50 feet)",
            "Bedrolls (4)",
            "Rations (10 days)",
            "Torches (20)",
            "Tinderbox",
            "Crowbar",
            "Hammer",
            "Pitons (10)",
            "Healing Potions (2)"
        ],
        party_funds=150,
        reputation={
            "Riverside Village": "friendly"
        },
        active_quests=[],
        completed_quests=[],
        notes="The party formed after meeting at the Riverside Tavern. They have proven themselves capable of working together and are gaining a reputation as reliable problem-solvers."
    )
    
    # Save party file with character references
    party_data = asdict(party)
    party_data['member_files'] = character_files
    
    party_filepath = os.path.join(player_data_dir, "party.json")
    with open(party_filepath, 'w', encoding='utf-8') as f:
        json.dump(party_data, f, indent=2, ensure_ascii=False)
    
    print("Created example party and characters:")
    print(f"  - Party file: party.json")
    for filename in character_files:
        print(f"  - Character file: {filename}")
    
    return character_files


def setup_initial_campaign_state(dm: DungeonMaster):
    """Setup the initial state for a new campaign"""
    # Try to load existing party, or create example party
    try:
        dm.load_party_from_file("party.json")
        print("Loaded existing party.")
    except FileNotFoundError:
        print("No existing party found. Creating example party...")
        create_example_party(dm.config.player_data_dir)
        dm.load_party_from_file("party.json")
    
    # Set initial location
    dm.set_current_location("Riverside Tavern")
    
    # Setup sample campaign content
    setup_sample_campaign(dm)
    
    print(f"\nCampaign initialized!")
    print(f"Current location: {dm.current_location}")
    print(f"Party loaded: {dm.party.name if dm.party else 'None'}")


def get_campaign_intro() -> str:
    """Get the introductory text for the campaign"""
    return """
Welcome to the village of Riverside! Your party of adventurers has just arrived at the Riverside Tavern, 
a warm and welcoming establishment that serves as the heart of this small farming community. 

The tavern is bustling with locals sharing stories over mugs of ale, and the smell of hearty stew fills the air. 
Outside, you can hear the gentle sound of the river flowing past the village, and in the distance, 
the dark outline of the Whispering Woods looms mysteriously on the horizon.

Your adventure begins here, where rumors of missing merchants, strange lights, and goblin raids 
have the villagers worried. What will your party choose to investigate first?
"""