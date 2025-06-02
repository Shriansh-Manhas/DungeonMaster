from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime


@dataclass
class PlayerCharacter:
    """Data model for a player character"""
    id: str
    name: str
    character_class: str
    level: int
    race: str
    background: str
    alignment: str
    stats: Dict[str, int]  # STR, DEX, CON, INT, WIS, CHA
    skills: List[str]
    equipment: List[str]
    backstory: str
    personality_traits: List[str]
    ideals: str
    bonds: str
    flaws: str
    hit_points: int
    armor_class: int
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def get_stat_modifier(self, stat: str) -> int:
        """Calculate ability modifier for a given stat"""
        stat_value = self.stats.get(stat, 10)
        return (stat_value - 10) // 2
    
    def get_summary(self) -> str:
        """Get a brief summary of the character"""
        return (
            f"{self.name}: Level {self.level} {self.race} {self.character_class} "
            f"(AC: {self.armor_class}, HP: {self.hit_points})"
        )
    
    def get_roleplay_info(self) -> str:
        """Get roleplay information for DM context"""
        traits = ", ".join(self.personality_traits) if self.personality_traits else "None"
        return (
            f"Background: {self.background}\n"
            f"Personality: {traits}\n"
            f"Ideals: {self.ideals}\n"
            f"Bonds: {self.bonds}\n"
            f"Flaws: {self.flaws}"
        )


@dataclass
class Party:
    """Data model for an adventuring party"""
    name: str
    members: List[PlayerCharacter]
    formation: str
    shared_equipment: List[str]
    party_funds: int
    reputation: Dict[str, str]  # location: reputation_level
    active_quests: List[str]
    completed_quests: List[str]
    notes: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def get_party_level(self) -> float:
        """Calculate average party level"""
        if not self.members:
            return 0
        return sum(member.level for member in self.members) / len(self.members)
    
    def get_class_composition(self) -> Dict[str, int]:
        """Get count of each class in the party"""
        composition = {}
        for member in self.members:
            class_name = member.character_class
            composition[class_name] = composition.get(class_name, 0) + 1
        return composition
    
    def get_summary(self) -> str:
        """Get a summary of the party"""
        if not self.members:
            return f"Party '{self.name}' has no members"
        
        avg_level = self.get_party_level()
        composition = self.get_class_composition()
        class_list = ", ".join([f"{count} {cls}" for cls, count in composition.items()])
        
        summary = [
            f"Party: {self.name}",
            f"Members: {len(self.members)} (Average Level: {avg_level:.1f})",
            f"Composition: {class_list}",
            f"Funds: {self.party_funds} gold"
        ]
        
        if self.active_quests:
            summary.append(f"Active Quests: {len(self.active_quests)}")
        
        return "\n".join(summary)
    
    def get_detailed_summary(self) -> str:
        """Get a detailed summary including all members"""
        summary = [self.get_summary(), ""]
        
        if self.members:
            summary.append("Members:")
            for member in self.members:
                summary.append(f"  - {member.get_summary()}")
        
        if self.formation:
            summary.extend(["", f"Formation: {self.formation}"])
        
        if self.active_quests:
            summary.extend(["", f"Active Quests: {', '.join(self.active_quests)}"])
        
        if self.reputation:
            summary.extend(["", "Reputation:"])
            for location, rep in self.reputation.items():
                summary.append(f"  - {location}: {rep}")
        
        return "\n".join(summary)