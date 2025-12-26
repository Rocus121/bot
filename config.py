import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = "llama-3.3-70b-versatile"  # Fisso nel codice
TEMPERATURE = 0.7
MAX_TOKENS = 2000

# File Paths
DATA_DIR = "data"
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")
INSTRUCTIONS_FILE = os.path.join(DATA_DIR, "agent_instructions.json")

# Default Instructions
DEFAULT_SYSTEM_PROMPT = "Sei un assistente AI utile e professionale."