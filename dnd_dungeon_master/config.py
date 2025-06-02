import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip loading .env file
    pass


class DMConfig:
    """Configuration management for the D&D Dungeon Master system"""
    
    def __init__(self):
        # Load API key from environment variable
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self.model_name = "openai/gpt-3.5-turbo"
        self.vector_db_path = "./dnd_vector_db"
        self.player_data_dir = "./player_data"
        
        # LLM settings
        self.temperature = 0.8
        self.max_tokens = 1000
        
        # Memory settings
        self.conversation_window = 10  # Keep last 10 exchanges
        
        # Vector store settings
        self.embedding_model = "text-embedding-ada-002"
        self.similarity_search_k = 5
        
        # Validate required environment variables
        if not self.openrouter_api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable must be set.\n"
                "Please set it in your environment or create a .env file with:\n"
                "OPENROUTER_API_KEY=your_api_key_here"
            )
    
    def validate_directories(self):
        """Ensure all required directories exist"""
        os.makedirs(self.vector_db_path, exist_ok=True)
        os.makedirs(self.player_data_dir, exist_ok=True)
    
    def get_llm_config(self) -> dict:
        """Get configuration for LLM initialization"""
        return {
            "openai_api_key": self.openrouter_api_key,
            "openai_api_base": self.openrouter_base_url,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_embeddings_config(self) -> dict:
        """Get configuration for embeddings initialization"""
        return {
            "openai_api_key": self.openrouter_api_key,
            "openai_api_base": self.openrouter_base_url,
            "model": self.embedding_model
        }