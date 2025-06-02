# D&D AI Dungeon Master

Ever wanted to play D&D but couldn't find a DM? Or maybe you're a DM who's tired of keeping track of a million NPCs and quest details? I built this AI-powered Dungeon Master to solve exactly those problems.

This isn't just another chatbot – it's a full-featured D&D companion that remembers your characters, tracks your campaigns, and generates rich, contextual stories that actually make sense with your party's abilities and backstories.

## Why I Built This

As someone who loves D&D but struggles to coordinate schedules with friends, I was frustrated by the lack of good solo or small-group options. Most AI tools either forget everything after a few messages or give generic responses that don't account for your specific character builds.

I wanted something that could:
- Remember my character's personality and backstory
- Track ongoing quests and relationships with NPCs
- Generate stories that actually consider my party composition
- Work offline once set up (no subscription required after initial API setup)

After months of tinkering with LangChain and various AI models, this is what I came up with.

## What Makes This Different

### It Actually Remembers Everything
Your characters, their relationships, ongoing quests, reputation in different towns – it's all stored locally and referenced in every interaction. The AI DM knows that Thorin doesn't trust magic users and that your party still owes money to the blacksmith in Riverside Village.

### Smart Context Awareness
Instead of generic responses, the AI considers your actual character sheets. It knows your wizard can't cast fireball yet, remembers that your rogue has thieves' tools, and won't suggest solutions that don't fit your party's capabilities.

### No Monthly Fees
Once you have an OpenRouter API key (which costs pennies per conversation), everything runs locally. Your campaign data belongs to you, stored in simple JSON files you can backup or modify.

### Built for Real D&D
This isn't a simplified version of D&D – it works with actual character sheets, tracks real stats, and handles complex party dynamics. I've been using it for my own campaigns for months.

## Getting Started

### What You'll Need
- Python 3.11+ (if you don't have it, download from python.org)
- An OpenRouter API key (get one free at openrouter.ai – you'll pay only for what you use, usually under $1/month for regular play)
- About 10 minutes to set everything up

### Quick Setup

I've tried to make this as painless as possible:

```bash
# 1. Grab the code
git clone https://github.com/yourusername/dnd-ai-dungeon-master.git
cd dnd-ai-dungeon-master

# 2. Set up the project (this creates all the folders and files you need)
python setup.py

# 3. Install the AI libraries
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Edit .env and paste your OpenRouter API key

# 5. Start playing!
python main.py
```

That's it. The first time you run it, it'll create example characters so you can jump right in and see how it works.

## How It Actually Works

### Your First Session
When you start the system, you'll find yourself at the Riverside Tavern with a party of four adventurers I created as examples. You can use them to try things out, or create your own characters by editing the JSON files in the `player_data` folder.

The AI knows each character's background, personality, and capabilities. Try typing something like:

```
We approach the barkeeper and ask about any interesting rumors
```

The AI DM will respond as Gareth the barkeeper, maybe mentioning the missing merchant caravan or strange lights in the Whispering Woods. It's pulling this information from the world database, not making it up on the spot.

### Creating Your Own Characters
Character sheets are stored as simple JSON files. I know, I know – JSON isn't the most user-friendly format, but it's easy to edit and backup. Here's what a character file looks like:

```json
{
  "name": "Your Character Name",
  "character_class": "Fighter",
  "level": 1,
  "race": "Human",
  "stats": {"STR": 15, "DEX": 13, "CON": 14, "INT": 12, "WIS": 10, "CHA": 8},
  "equipment": ["Chain Mail", "Shield", "Longsword"],
  "backstory": "Write whatever you want here",
  "personality_traits": ["I'm brave but reckless", "I always help those in need"]
}
```

The AI reads all of this and incorporates it into the story. Your character's personality traits actually influence how NPCs react to them.

### Commands You Can Use
- `party` – See your full party stats and status
- `location` – Get details about where you are
- `context` – Quick summary of your current situation
- `help` – Show available commands

For everything else, just describe what you want to do in plain English. The AI is pretty good at understanding intent.

## Under the Hood (For the Curious)

I built this using LangChain because it makes working with AI models much more manageable. Here's the basic architecture:

### The Smart Parts
- **Vector Database**: All NPCs, quests, and locations are stored in ChromaDB with embeddings. When you do something, it automatically finds relevant context.
- **Memory Management**: The AI remembers your last 10 exchanges, plus pulls in relevant historical context based on what's happening.
- **Character Integration**: Your character sheets aren't just flavor text – the AI actually considers your stats, equipment, and background when generating responses.

### The Simple Parts
- **Character Storage**: JSON files you can edit with any text editor
- **Configuration**: Everything configurable through a `.env` file
- **Local Data**: Everything except the AI model runs on your machine

The project structure is intentionally modular. If you want to modify how NPCs work, you edit one file. If you want to change how character data is stored, that's in a different file. I spent a lot of time organizing this so it wouldn't become an unmaintainable mess.

## Real Examples from My Games

Here are some actual interactions I've had with the system:

**Me**: "Pip tries to pickpocket the merchant while the others distract him"

**AI DM**: "As Thorin loudly argues about the price of chainmail, Pip notices the merchant's coin purse hanging loosely from his belt. Roll a Sleight of Hand check. Given Pip's Criminal background and the merchant's distraction, you have advantage on this roll."

The AI remembered that Pip is a rogue with a criminal background, knows about advantage mechanics, and incorporated the distraction plan into the skill check.

**Me**: "We camp for the night in the forest"

**AI DM**: "Brother Marcus offers to take first watch, his holy symbol glowing faintly as he whispers evening prayers. Elaria suggests using her familiar to scout the perimeter. The forest is unusually quiet – even Pip, who grew up on the streets, finds the silence unsettling."

It referenced three different character backgrounds in one response and set up potential plot hooks based on the unusual quiet.

## Customizing Everything

### Changing the AI Model
Want to use a different model? Edit `config.py`:

```python
self.model_name = "anthropic/claude-3-haiku"  # or whatever OpenRouter supports
```

I've tested it with GPT-3.5, GPT-4, and Claude models. GPT-3.5 is the sweet spot of cost vs. quality for most games.

### Adding Your Own Content
The example campaign is just to get you started. You can add new NPCs, locations, and quests either by editing the JSON files directly or using the built-in methods:

```python
# Add a new NPC
dm.add_npc_to_story(
    name="Captain Sarah Blackwater",
    description="A stern naval officer with a mysterious past",
    personality="professional but hiding secrets",
    location="Harbor District",
    role="harbor master"
)
```

### Campaign Persistence
Everything saves automatically. When you close the program and restart it later, all your progress is exactly where you left it. Your characters remember who they've met, what quests they're on, and how different NPCs feel about them.

## What I'm Still Working On

This is a personal project I've been building in my spare time, so there are definitely areas for improvement:

- **Better Character Creation**: The JSON editing works but isn't very user-friendly
- **Map Integration**: I'd love to add simple ASCII maps or even visual maps
- **Dice Rolling**: Right now the AI asks for rolls but doesn't actually roll them
- **Combat System**: Basic combat works but could be more sophisticated
- **Voice Integration**: Text-to-speech would make this feel more immersive

## Troubleshooting

### "API Key Error"
Make sure your `.env` file has your actual OpenRouter API key, not the placeholder text. The format should be:
```
OPENROUTER_API_KEY=sk-or-your-actual-key-here
```

### "Import Error" or Package Issues
This usually means the AI libraries didn't install correctly. Try:
```bash
pip uninstall langchain langchain-openai langchain-community -y
pip install -r requirements.txt
```

### "The AI Responses Don't Make Sense"
Check that your character files are valid JSON. A missing comma or bracket can confuse the context system. Use an online JSON validator if you're not sure.

### "Everything Disappeared"
Your data is in the `player_data` and `dnd_vector_db` folders. If you accidentally delete these, just run `python main.py` again and it'll recreate the examples.

## Contributing

This started as a personal project, but I'd love to see what others build with it. If you add something cool or fix a bug, please submit a pull request. I'm especially interested in:

- Better user interfaces for character creation
- Additional AI model integrations
- Combat system improvements
- Pre-built campaign modules

## A Personal Note

I built this because I love D&D but life often gets in the way of regular gaming sessions. If you're in the same boat, I hope this helps you get back to adventuring. It's not perfect, and it's definitely not a replacement for playing with friends, but it's been a lot of fun to build and use.

The code is open source because I believe tools like this should be accessible to everyone, not locked behind expensive subscriptions. If you build something cool with it, I'd love to hear about it.

Happy adventuring!

---

*This project is a fan creation and isn't affiliated with Wizards of the Coast or the official D&D brand. It's built by a D&D enthusiast for other D&D enthusiasts.*