# How Character Files Work

The AI DM needs to know about your characters to run a good game. Instead of some complicated database, I went with simple JSON files that you can edit with any text editor. Here's how it all works and what you can customize.

## The Basic Idea

Each character is stored in its own JSON file in the `player_data` folder. Your party is defined in a `party.json` file that references all the individual character files. This way you can have characters who aren't currently in the party, or easily move characters between different campaigns.

The AI reads all this information when generating responses, so your character's background, personality, and equipment actually matter in the story.

## Character File Structure

Here's what a complete character file looks like. I'll use Thorin as an example since he's one of the starting characters:

### thorin_ironforge.json

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Thorin Ironforge",
  "character_class": "Fighter",
  "level": 3,
  "race": "Dwarf",
  "background": "Soldier",
  "alignment": "Lawful Good",
  "stats": {
    "STR": 16,
    "DEX": 12,
    "CON": 15,
    "INT": 10,
    "WIS": 14,
    "CHA": 8
  },
  "skills": [
    "Athletics",
    "Intimidation", 
    "Perception",
    "Survival"
  ],
  "equipment": [
    "Chain Mail",
    "Shield",
    "Warhammer",
    "Handaxe (2)",
    "Explorers Pack",
    "Military Rank Insignia"
  ],
  "backstory": "A veteran soldier who served in the King's Guard for over a decade. After witnessing corruption in the ranks, he left to seek true honor as an adventurer.",
  "personality_traits": [
    "I face problems head-on with direct, simple solutions",
    "I enjoy being strong and like breaking things"
  ],
  "ideals": "Responsibility. I do what I must and obey just authority.",
  "bonds": "My honor is my life. I would rather die than compromise my principles.",
  "flaws": "I have little respect for anyone who is not a proven warrior.",
  "hit_points": 29,
  "armor_class": 18,
  "created_at": "2024-01-15T10:30:00"
}
```

## What Each Field Does

**Basic Info:**
- `name`: What everyone calls your character
- `character_class`: Fighter, Wizard, Rogue, etc. The AI knows D&D classes and their abilities
- `level`: Your character level (affects what the AI thinks you can do)
- `race`: Dwarf, Elf, Human, etc. This influences how NPCs react to you
- `background`: Your character's pre-adventuring life. Really important for roleplay

**Game Mechanics:**
- `stats`: The six D&D ability scores. The AI actually uses these for skill checks and story beats
- `skills`: What your character is good at. The AI will suggest using these when appropriate
- `equipment`: What you're carrying. The AI knows you can't cast spells without a focus or pick locks without thieves' tools
- `hit_points` and `armor_class`: Your survivability stats

**Roleplay Elements:**
- `backstory`: Free-form text about your character's history
- `personality_traits`: How your character acts (the AI uses these a lot)
- `ideals`: What your character believes in
- `bonds`: What your character cares about
- `flaws`: Your character's weaknesses (makes for better stories)

**System Stuff:**
- `id`: Unique identifier (auto-generated, don't worry about it)
- `alignment`: Your character's moral compass
- `created_at`: When the character was made (also auto-generated)

## A Simpler Example

If all that JSON looks intimidating, here's a minimal character that would still work fine:

### simple_character.json

```json
{
  "name": "Robin Swift",
  "character_class": "Rogue",
  "level": 1,
  "race": "Human",
  "background": "Criminal",
  "alignment": "Chaotic Good",
  "stats": {"STR": 10, "DEX": 16, "CON": 12, "INT": 14, "WIS": 13, "CHA": 15},
  "skills": ["Stealth", "Sleight of Hand", "Deception"],
  "equipment": ["Leather Armor", "Shortsword", "Thieves' Tools"],
  "backstory": "A former pickpocket trying to go straight.",
  "personality_traits": ["Quick with jokes", "Always looking for exits"],
  "ideals": "Everyone deserves a second chance.",
  "bonds": "I owe everything to my mentor who saved me from the streets.",
  "flaws": "I can't resist a good heist.",
  "hit_points": 10,
  "armor_class": 13
}
```

The system will fill in reasonable defaults for anything you don't specify.

## How Party Management Works

Your party is defined in `party.json`, which looks like this:

### party.json

```json
{
  "name": "The Brave Companions",
  "member_files": [
    "thorin_ironforge.json",
    "elaria_moonwhisper.json",
    "pip_lightfingers.json",
    "brother_marcus.json"
  ],
  "formation": "Thorin takes point, Elaria and Marcus in the middle, Pip scouts ahead or brings up the rear",
  "shared_equipment": [
    "Rope (50 feet)",
    "Bedrolls (4)",
    "Rations (10 days)",
    "Torches (20)",
    "Tinderbox"
  ],
  "party_funds": 347,
  "reputation": {
    "Riverside Village": "friendly",
    "Whispering Woods": "neutral",
    "Bandit Camps": "hostile"
  },
  "active_quests": [
    "The Missing Merchant",
    "Goblin Raids"
  ],
  "completed_quests": [
    "Rat Problem in the Tavern Cellar"
  ],
  "notes": "The party formed after meeting at the Riverside Tavern. They have proven themselves capable of working together and are gaining a reputation as reliable problem-solvers.",
  "created_at": "2024-01-15T10:30:00"
}
```

**What This Controls:**
- `member_files`: Which character files are in your current party
- `formation`: How you approach situations (the AI considers this)
- `shared_equipment`: Stuff the whole party can use
- `party_funds`: Money you all share
- `reputation`: How different groups feel about you
- `active_quests`: What you're currently working on
- `completed_quests`: Your past accomplishments
- `notes`: Free-form party history

## Editing Your Characters

### Using a Text Editor
Any text editor works, but I recommend something that can validate JSON:
- **VS Code** (free, great JSON support)
- **Notepad++** (Windows, free)
- **Sublime Text** (cross-platform, has free trial)

### Online JSON Validators
If you're not sure your JSON is correct, paste it into [jsonlint.com](https://jsonlint.com/) to check for errors.

### Common Mistakes
- **Missing commas**: Every line except the last needs a comma
- **Unmatched quotes**: Strings need to be in "double quotes"
- **Wrong brackets**: `{}` for objects, `[]` for lists
- **Trailing commas**: Don't put a comma after the last item in a list

## Creating New Characters

### Method 1: Copy and Modify
The easiest way is to copy an existing character file and change the details:

```bash
cp thorin_ironforge.json my_new_character.json
# Edit my_new_character.json with your character's details
```

### Method 2: Use the Template
Here's a template you can start with:

```json
{
  "name": "Your Character Name",
  "character_class": "Fighter/Wizard/Rogue/Cleric/etc",
  "level": 1,
  "race": "Human/Elf/Dwarf/etc",
  "background": "Folk Hero/Criminal/Sage/etc",
  "alignment": "Lawful Good/Chaotic Neutral/etc",
  "stats": {
    "STR": 10, "DEX": 10, "CON": 10,
    "INT": 10, "WIS": 10, "CHA": 10
  },
  "skills": ["Skill1", "Skill2", "Skill3"],
  "equipment": ["Item1", "Item2", "Item3"],
  "backstory": "Your character's background story",
  "personality_traits": ["Trait 1", "Trait 2"],
  "ideals": "What your character believes",
  "bonds": "What your character cares about",
  "flaws": "Your character's weakness",
  "hit_points": 8,
  "armor_class": 10
}
```

### Method 3: Let the System Create Examples
Run the program and it'll create example characters you can modify.

## Tips for Better Characters

### Make Personality Matter
The AI pays a lot of attention to personality traits. Instead of:
```
"personality_traits": ["Brave", "Smart"]
```

Try:
```
"personality_traits": [
  "I never back down from a challenge, even when I should",
  "I quote old military sayings that nobody else understands"
]
```

### Give Them Real Equipment
The AI knows what different items do. Instead of just "Sword", try:
```
"equipment": [
  "Longsword (family heirloom with engravings)",
  "Shield (dented from many battles)",
  "Chain Mail (well-maintained)",
  "Healing Potion (saved for emergencies)",
  "Military Rank Insignia (from previous service)"
]
```

### Connect to the World
Reference the campaign setting in your backstory:
```
"backstory": "Grew up in Riverside Village, always wondered about the strange lights people reported seeing in Whispering Woods."
```

This gives the AI hooks to connect your character to the ongoing story.

### Use Flaws Creatively
Flaws make characters interesting and give the AI opportunities for drama:
- "I can't resist helping someone in trouble, even if it's obviously a trap"
- "I have a gambling problem and will bet on anything"
- "I trust authority figures too much, even when they're clearly corrupt"

## Directory Structure

Your player data should look like this:

```
./player_data/
├── party.json                 # Party definition
├── thorin_ironforge.json     # Individual characters
├── elaria_starweaver.json
├── pip_lightfingers.json
├── brother_marcus.json
└── my_custom_character.json  # Your additions
```

## What Happens When You Change Things

### During Play
If you edit character files while the game is running, you'll need to restart for changes to take effect. The AI loads everything at startup.

### Between Sessions
All changes persist automatically. If you level up, get new equipment, or change reputation, edit the appropriate files and it'll be there next time you play.

### Backup Your Characters
Since these are just files, backing up is simple:
```bash
# Backup your entire campaign
tar -czf my_campaign_backup.tar.gz player_data/

# Or just copy the folder
cp -r player_data/ player_data_backup/
```

## Advanced Customization

### Custom Attributes
You can add your own fields to character files. The AI won't use them directly, but they'll be preserved:

```json
{
  "name": "Custom Character",
  // ... standard fields ...
  "custom_notes": "Has a pet raven named Edgar",
  "favorite_food": "Honey cakes",
  "secret_fear": "Afraid of the dark"
}
```

### Multiple Campaigns
Use different folders for different campaigns:
```bash
# Campaign 1
PLAYER_DATA_DIR=./campaign_1 python main.py

# Campaign 2
PLAYER_DATA_DIR=./campaign_2 python main.py
```

### Shared Characters
Characters can appear in multiple campaigns by copying their files between player_data directories.

The whole system is designed to be flexible and easy to modify. Don't be afraid to experiment – you can always restore from a backup if something breaks.