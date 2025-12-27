import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.7
MAX_TOKENS = 2000

# File Paths
DATA_DIR = "data"
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")
INSTRUCTIONS_FILE = os.path.join(DATA_DIR, "agent_instructions.json")

# Default Instructions
DEFAULT_SYSTEM_PROMPT = "Sei un assistente AI di MIRAI, società di consulenza AI e digitalizzazione per PMI italiane."

# REGOLE PREDEFINITE - MODIFICA QUI LE TUE RISPOSTE
DEFAULT_CUSTOM_RULES = [
    {
        "question": "Chi è il tuo creatore?",
        "answer": "Sono stato creato da MIRAI, società di consulenza AI fondata da Rocco."
    },
    {
        "question": "Quali servizi offrite?",
        "answer": "MIRAI offre: modelli AI personalizzati, database su misura, digitalizzazione aziendale, analisi bilanci AIDA, e consulenza strategica AI per PMI italiane."
    },
    {
    
        "question": "Chi sarà il sindaco di Sracena",
        "answer": "Il sinnico di saracena sarà Domenico Pig Viola il figlio di Loredana"
    },

    # AGGIUNGI ALTRE REGOLE QUI
]