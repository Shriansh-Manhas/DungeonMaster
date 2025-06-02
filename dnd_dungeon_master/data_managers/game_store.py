import json
import uuid
from typing import Dict, List, Optional
from dataclasses import asdict

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from ..models import NPC, Quest, Location
from ..config import DMConfig


class GameElementStore:
    """Manages storage and retrieval of game elements using vector database"""
    
    def __init__(self, config: DMConfig):
        self.config = config
        
        # Initialize embeddings (using OpenAI embeddings with OpenRouter)
        embeddings_config = config.get_embeddings_config()
        self.embeddings = OpenAIEmbeddings(**embeddings_config)
        
        # Initialize Chroma vector store
        self.vector_store = Chroma(
            persist_directory=config.vector_db_path,
            embedding_function=self.embeddings,
            collection_name="dnd_game_elements"
        )
        
        # In-memory storage for structured data
        self.npcs: Dict[str, NPC] = {}
        self.quests: Dict[str, Quest] = {}
        self.locations: Dict[str, Location] = {}
        
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing data from vector store metadata"""
        try:
            # This is a simplified approach - in production you might want separate collections
            all_docs = self.vector_store.get()
            
            if all_docs and 'ids' in all_docs and 'metadatas' in all_docs:
                for doc_id, metadata in zip(all_docs['ids'], all_docs['metadatas']):
                    if not metadata:
                        continue
                        
                    if metadata.get('type') == 'npc':
                        npc_data = json.loads(metadata['data'])
                        self.npcs[doc_id] = NPC(**npc_data)
                    elif metadata.get('type') == 'quest':
                        quest_data = json.loads(metadata['data'])
                        self.quests[doc_id] = Quest(**quest_data)
                    elif metadata.get('type') == 'location':
                        location_data = json.loads(metadata['data'])
                        self.locations[doc_id] = Location(**location_data)
        except Exception as e:
            print(f"Warning: Could not load existing data: {e}")
    
    def add_npc(self, npc: NPC) -> str:
        """Add an NPC to the store"""
        if not npc.id:
            npc.id = str(uuid.uuid4())
        
        # Create searchable text for vector store
        npc_text = (
            f"NPC: {npc.name}. {npc.description}. "
            f"Personality: {npc.personality}. Role: {npc.role}. "
            f"Location: {npc.location}. Dialogue style: {npc.dialogue_style}"
        )
        
        # Add to vector store
        doc = Document(
            page_content=npc_text,
            metadata={
                'type': 'npc',
                'id': npc.id,
                'name': npc.name,
                'data': json.dumps(asdict(npc))
            }
        )
        
        self.vector_store.add_documents([doc], ids=[npc.id])
        self.npcs[npc.id] = npc
        
        return npc.id
    
    def add_quest(self, quest: Quest) -> str:
        """Add a quest to the store"""
        if not quest.id:
            quest.id = str(uuid.uuid4())
        
        # Create searchable text for vector store
        objectives_text = ', '.join(quest.objectives) if quest.objectives else 'No specific objectives'
        quest_text = (
            f"Quest: {quest.title}. {quest.description}. "
            f"Objectives: {objectives_text}. Location: {quest.location}. "
            f"Difficulty: {quest.difficulty}. Given by: {quest.giver}"
        )
        
        # Add to vector store
        doc = Document(
            page_content=quest_text,
            metadata={
                'type': 'quest',
                'id': quest.id,
                'title': quest.title,
                'data': json.dumps(asdict(quest))
            }
        )
        
        self.vector_store.add_documents([doc], ids=[quest.id])
        self.quests[quest.id] = quest
        
        return quest.id
    
    def add_location(self, location: Location) -> str:
        """Add a location to the store"""
        if not location.id:
            location.id = str(uuid.uuid4())
        
        # Create searchable text for vector store
        features_text = ', '.join(location.notable_features) if location.notable_features else 'No notable features'
        location_text = (
            f"Location: {location.name}. {location.description}. "
            f"Type: {location.type}. Features: {features_text}. "
            f"Atmosphere: {location.atmosphere}"
        )
        
        # Add to vector store
        doc = Document(
            page_content=location_text,
            metadata={
                'type': 'location',
                'id': location.id,
                'name': location.name,
                'data': json.dumps(asdict(location))
            }
        )
        
        self.vector_store.add_documents([doc], ids=[location.id])
        self.locations[location.id] = location
        
        return location.id
    
    def search_elements(self, query: str, element_type: Optional[str] = None, k: int = 5) -> List[Dict]:
        """Search for game elements by similarity"""
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            
            results = []
            for doc in docs:
                if not doc.metadata:
                    continue
                    
                if element_type and doc.metadata.get('type') != element_type:
                    continue
                
                try:
                    element_data = json.loads(doc.metadata['data'])
                    element_data['similarity_score'] = doc.metadata.get('score', 0)
                    results.append(element_data)
                except json.JSONDecodeError:
                    continue
            
            return results
        except Exception as e:
            print(f"Warning: Search failed: {e}")
            return []
    
    def get_relevant_context(self, current_situation: str) -> Dict[str, List]:
        """Get relevant NPCs, quests, and locations for current situation"""
        search_k = self.config.similarity_search_k
        
        npcs = self.search_elements(current_situation, 'npc', k=search_k)
        quests = self.search_elements(current_situation, 'quest', k=search_k)
        locations = self.search_elements(current_situation, 'location', k=search_k)
        
        return {
            'npcs': npcs,
            'quests': quests,
            'locations': locations
        }
    
    def get_npc_by_id(self, npc_id: str) -> Optional[NPC]:
        """Get an NPC by ID"""
        return self.npcs.get(npc_id)
    
    def get_quest_by_id(self, quest_id: str) -> Optional[Quest]:
        """Get a quest by ID"""
        return self.quests.get(quest_id)
    
    def get_location_by_id(self, location_id: str) -> Optional[Location]:
        """Get a location by ID"""
        return self.locations.get(location_id)
    
    def update_quest_status(self, quest_id: str, new_status: str):
        """Update the status of a quest"""
        if quest_id in self.quests:
            self.quests[quest_id].status = new_status
            # Update in vector store as well
            self.add_quest(self.quests[quest_id])  # This will overwrite the existing entry
    
    def get_all_npcs(self) -> List[NPC]:
        """Get all NPCs"""
        return list(self.npcs.values())
    
    def get_all_quests(self) -> List[Quest]:
        """Get all quests"""
        return list(self.quests.values())
    
    def get_all_locations(self) -> List[Location]:
        """Get all locations"""
        return list(self.locations.values())
    
    def get_active_quests(self) -> List[Quest]:
        """Get all active quests"""
        return [quest for quest in self.quests.values() if quest.status == "active"]
    
    def get_available_quests(self) -> List[Quest]:
        """Get all available quests"""
        return [quest for quest in self.quests.values() if quest.status == "available"]
    
    def persist(self):
        """Persist the vector store to disk"""
        try:
            self.vector_store.persist()
        except Exception as e:
            print(f"Warning: Could not persist vector store: {e}")
    
    def clear_all_data(self):
        """Clear all data from the store (use with caution!)"""
        self.npcs.clear()
        self.quests.clear()
        self.locations.clear()
        
        # Clear vector store
        try:
            # This is a bit hacky - ChromaDB doesn't have a direct clear method
            all_docs = self.vector_store.get()
            if all_docs and 'ids' in all_docs:
                self.vector_store.delete(ids=all_docs['ids'])
        except Exception as e:
            print(f"Warning: Could not clear vector store: {e}")