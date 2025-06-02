"""
D&D AI Dungeon Master

A sophisticated Dungeons & Dragons Dungeon Master powered by LangChain and OpenAI models.
"""

__version__ = "1.0.0"

from .config import DMConfig
from .core.dungeon_master import DungeonMaster

__all__ = ['DMConfig', 'DungeonMaster']
