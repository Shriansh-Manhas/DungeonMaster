from typing import Optional, Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory

from ..config import DMConfig
from ..data_managers import GameElementStore
from ..data_managers import PlayerDataManager
from ..models import Party
from ..models import NPC, Quest, Location


class DungeonMaster:
    """Main Dungeon Master class that handles story generation and player interaction"""
    
    def __init__(self, config: DMConfig, player_data_dir: str = None):
        self.config = config
        if player_data_dir is None:
            player_data_dir = config.player_data_dir
            
        self.game_store = GameElementStore(config)
        self.player_manager = PlayerDataManager(player_data_dir)
        
        # Initialize ChatOpenAI with OpenRouter
        llm_config = config.get_llm_config()
        self.llm = ChatOpenAI(**llm_config)
        
        # Conversation memory
        self.memory = ConversationBufferWindowMemory(
            k=config.conversation_window,
            return_messages=True
        )
        
        # Game state
        self.current_location = None
        self.party: Optional[Party] = None
        
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Setup the prompt templates for the DM"""
        
        system_template = """You are an expert Dungeon Master for a Dungeons & Dragons campaign. Your role is to:

1. Generate engaging, immersive narrative descriptions
2. Control NPCs and their dialogue
3. Present quest opportunities and manage story progression
4. Respond to player actions with appropriate consequences
5. Maintain consistency with the established world and characters

IMPORTANT GUIDELINES:
- Always stay in character as the DM
- Be descriptive but concise
- Ask for dice rolls when appropriate
- Make the story engaging and interactive
- Use the provided context about NPCs, quests, and locations to maintain consistency
- Never break the fourth wall or mention game mechanics explicitly to players
- Consider the party's abilities, equipment, and personalities when crafting scenarios
- Reference character backstories and motivations when relevant

Current Game Context:
{context}

Conversation History:
{chat_history}"""

        human_template = """Player Action/Response: {player_input}

As the DM, respond to this player action. Consider the current context and maintain narrative consistency."""

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template)
        ])
    
    def load_party_from_file(self, party_filename: str = "party.json"):
        """Load party data from file"""
        try:
            self.party = self.player_manager.load_party(party_filename)
            print(f"Loaded party: {self.party.name} with {len(self.party.members)} members")
            for member in self.party.members:
                print(f"  - {member.name} (Level {member.level} {member.race} {member.character_class})")
        except FileNotFoundError:
            print(f"Party file '{party_filename}' not found.")
            raise
        except Exception as e:
            print(f"Error loading party: {e}")
            raise
    
    def set_current_location(self, location_name: str):
        """Set the current location for the party"""
        locations = self.game_store.search_elements(location_name, 'location', k=1)
        if locations:
            self.current_location = locations[0]['name']
        else:
            self.current_location = location_name
    
    def get_party_summary(self) -> str:
        """Get a summary of the current party"""
        if not self.party:
            return "No party loaded"
        
        return self.party.get_detailed_summary()
    
    def generate_response(self, player_input: str) -> str:
        """Generate DM response to player input"""
        
        # Get relevant context based on player input and current situation
        situation_context = f"{player_input} Current location: {self.current_location}"
        relevant_context = self.game_store.get_relevant_context(situation_context)
        
        # Format context for the prompt
        context_text = self._format_context(relevant_context)
        
        # Get chat history as string
        chat_history = "\n".join([
            f"{'Player' if isinstance(msg, HumanMessage) else 'DM'}: {msg.content}"
            for msg in self.memory.chat_memory.messages[-self.config.conversation_window:]
        ])
        
        # Create the formatted prompt
        formatted_prompt = self.prompt_template.format(
            context=context_text,
            chat_history=chat_history,
            player_input=player_input
        )
        
        # Generate response
        response = self.llm.invoke(formatted_prompt)
        
        # Update memory
        self.memory.chat_memory.add_user_message(player_input)
        self.memory.chat_memory.add_ai_message(response.content)
        
        return response.content
    
    def _format_context(self, context: Dict[str, List]) -> str:
        """Format the relevant context for the prompt"""
        formatted = []
        
        if context['locations']:
            formatted.append("RELEVANT LOCATIONS:")
            for loc in context['locations']:
                formatted.append(f"- {loc['name']}: {loc['description']}")
                if loc.get('atmosphere'):
                    formatted.append(f"  Atmosphere: {loc['atmosphere']}")
        
        if context['npcs']:
            formatted.append("\nRELEVANT NPCs:")
            for npc in context['npcs']:
                formatted.append(f"- {npc['name']} ({npc['role']}): {npc['description']}")
                formatted.append(f"  Personality: {npc['personality']}")
                formatted.append(f"  Dialogue Style: {npc['dialogue_style']}")
                formatted.append(f"  Relationship to Party: {npc['relationship_to_party']}")
        
        if context['quests']:
            formatted.append("\nRELEVANT QUESTS:")
            for quest in context['quests']:
                formatted.append(f"- {quest['title']} (Status: {quest['status']}): {quest['description']}")
                if quest.get('objectives'):
                    formatted.append(f"  Objectives: {', '.join(quest['objectives'])}")
                formatted.append(f"  Difficulty: {quest['difficulty']}")
        
        if self.current_location:
            formatted.append(f"\nCURRENT LOCATION: {self.current_location}")
        
        if self.party:
            formatted.append(f"\nPARTY INFORMATION:")
            formatted.append(f"Party Name: {self.party.name}")
            formatted.append(f"Average Level: {self.party.get_party_level():.1f}")
            formatted.append(f"Members ({len(self.party.members)}):")
            
            for member in self.party.members:
                formatted.append(f"  - {member.name} (Level {member.level} {member.race} {member.character_class})")
                formatted.append(f"    AC: {member.armor_class}, HP: {member.hit_points}")
                formatted.append(f"    Background: {member.background}")
                
                # Add key stats
                key_stats = []
                for stat, value in member.stats.items():
                    modifier = member.get_stat_modifier(stat)
                    key_stats.append(f"{stat} {value}({modifier:+d})")
                formatted.append(f"    Stats: {', '.join(key_stats)}")
                
                # Add personality info
                if member.personality_traits:
                    traits = ', '.join(member.personality_traits[:2])  # Limit to first 2
                    formatted.append(f"    Personality: {traits}")
                
                if member.equipment:
                    equipment = ', '.join(member.equipment[:3])  # Limit to first 3 items
                    formatted.append(f"    Key Equipment: {equipment}")
            
            if self.party.active_quests:
                formatted.append(f"\nActive Quests: {', '.join(self.party.active_quests)}")
            
            formatted.append(f"Party Funds: {self.party.party_funds} gold")
            formatted.append(f"Formation: {self.party.formation}")
            
            if self.party.reputation:
                formatted.append("Reputation:")
                for location, rep in self.party.reputation.items():
                    formatted.append(f"  - {location}: {rep}")
        
        return "\n".join(formatted) if formatted else "No specific context available."
    
    def add_npc_to_story(self, name: str, description: str, personality: str, 
                        location: str, role: str, relationship: str = "neutral",
                        dialogue_style: str = "formal") -> str:
        """Add a new NPC to the story"""
        npc = NPC(
            id="",
            name=name,
            description=description,
            personality=personality,
            location=location,
            role=role,
            relationship_to_party=relationship,
            dialogue_style=dialogue_style
        )
        return self.game_store.add_npc(npc)
    
    def add_quest_to_story(self, title: str, description: str, giver: str,
                          objectives: List[str], rewards: str, difficulty: str,
                          location: str, status: str = "available") -> str:
        """Add a new quest to the story"""
        quest = Quest(
            id="",
            title=title,
            description=description,
            giver=giver,
            status=status,
            objectives=objectives,
            rewards=rewards,
            difficulty=difficulty,
            location=location
        )
        return self.game_store.add_quest(quest)
    
    def add_location_to_story(self, name: str, description: str, location_type: str,
                             features: List[str], connected_locations: List[str] = None,
                             atmosphere: str = "neutral") -> str:
        """Add a new location to the story"""
        location = Location(
            id="",
            name=name,
            description=description,
            type=location_type,
            notable_features=features,
            connected_locations=connected_locations or [],
            npcs_present=[],
            quests_available=[],
            atmosphere=atmosphere
        )
        return self.game_store.add_location(location)
    
    def update_quest_status(self, quest_title: str, new_status: str):
        """Update the status of a quest by title"""
        # Find quest by title
        for quest in self.game_store.get_all_quests():
            if quest.title.lower() == quest_title.lower():
                self.game_store.update_quest_status(quest.id, new_status)
                
                # Update party's active quests if applicable
                if self.party:
                    if new_status == "active" and quest_title not in self.party.active_quests:
                        self.party.active_quests.append(quest_title)
                    elif new_status in ["completed", "failed"] and quest_title in self.party.active_quests:
                        self.party.active_quests.remove(quest_title)
                        if new_status == "completed":
                            self.party.completed_quests.append(quest_title)
                
                return True
        return False
    
    def get_current_context_summary(self) -> str:
        """Get a summary of the current game state"""
        summary = []
        
        if self.current_location:
            summary.append(f"Current Location: {self.current_location}")
        
        if self.party:
            summary.append(f"Party: {self.party.name} ({len(self.party.members)} members)")
            
            if self.party.active_quests:
                summary.append(f"Active Quests: {', '.join(self.party.active_quests)}")
        
        # Get nearby NPCs
        if self.current_location:
            nearby_npcs = self.game_store.search_elements(self.current_location, 'npc', k=3)
            if nearby_npcs:
                npc_names = [npc['name'] for npc in nearby_npcs]
                summary.append(f"Nearby NPCs: {', '.join(npc_names)}")
        
        return "\n".join(summary) if summary else "No current context available."