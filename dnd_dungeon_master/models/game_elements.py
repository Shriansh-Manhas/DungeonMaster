from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class NPC:
    """Data model for Non-Player Characters"""
    id: str
    name: str
    description: str
    personality: str
    location: str
    role: str
    relationship_to_party: str
    dialogue_style: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def get_context_summary(self) -> str:
        """Get summary for DM context"""
        return (
            f"{self.name} ({self.role}): {self.description} "
            f"Personality: {self.personality}. Located in {self.location}. "
            f"Relationship to party: {self.relationship_to_party}"
        )


@dataclass
class Quest:
    """Data model for quests and adventures"""
    id: str
    title: str
    description: str
    giver: str
    status: str  # "available", "active", "completed", "failed"
    objectives: List[str]
    rewards: str
    difficulty: str
    location: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def get_context_summary(self) -> str:
        """Get summary for DM context"""
        obj_text = "; ".join(self.objectives) if self.objectives else "No specific objectives"
        return (
            f"Quest '{self.title}' (Status: {self.status}): {self.description} "
            f"Given by {self.giver}. Objectives: {obj_text}. "
            f"Difficulty: {self.difficulty}. Rewards: {self.rewards}"
        )
    
    def is_active(self) -> bool:
        """Check if quest is currently active"""
        return self.status == "active"
    
    def is_available(self) -> bool:
        """Check if quest is available to accept"""
        return self.status == "available"
    
    def is_completed(self) -> bool:
        """Check if quest is completed"""
        return self.status == "completed"


@dataclass
class Location:
    """Data model for locations in the game world"""
    id: str
    name: str
    description: str
    type: str  # "town", "dungeon", "wilderness", "building"
    notable_features: List[str]
    connected_locations: List[str]
    npcs_present: List[str]
    quests_available: List[str]
    atmosphere: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def get_context_summary(self) -> str:
        """Get summary for DM context"""
        features_text = ", ".join(self.notable_features) if self.notable_features else "No notable features"
        return (
            f"Location '{self.name}' ({self.type}): {self.description} "
            f"Notable features: {features_text}. Atmosphere: {self.atmosphere}"
        )
    
    def get_detailed_description(self) -> str:
        """Get detailed description for scene setting"""
        description = [
            f"Location: {self.name}",
            f"Type: {self.type.title()}",
            f"Description: {self.description}",
            f"Atmosphere: {self.atmosphere}"
        ]
        
        if self.notable_features:
            description.extend([
                "Notable Features:",
                *[f"  - {feature}" for feature in self.notable_features]
            ])
        
        if self.connected_locations:
            description.extend([
                "Connected to:",
                *[f"  - {location}" for location in self.connected_locations]
            ])
        
        return "\n".join(description)