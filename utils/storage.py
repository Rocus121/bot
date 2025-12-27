import json
import os
from config import (
    DATA_DIR, 
    CONVERSATIONS_FILE, 
    INSTRUCTIONS_FILE, 
    DEFAULT_SYSTEM_PROMPT,
    DEFAULT_CUSTOM_RULES
)

class Storage:
    @staticmethod
    def ensure_data_dir():
        """Crea cartella data se non esiste"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
    
    @staticmethod
    def load_conversations():
        """Carica conversazioni da JSON"""
        Storage.ensure_data_dir()
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_conversations(conversations):
        """Salva conversazioni su JSON"""
        Storage.ensure_data_dir()
        with open(CONVERSATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_instructions():
        """Carica istruzioni SEMPRE da config.py"""
        Storage.ensure_data_dir()
        
        # IGNORA il file JSON, usa SEMPRE config.py
        return {
            "system_prompt": DEFAULT_SYSTEM_PROMPT,
            "custom_rules": DEFAULT_CUSTOM_RULES
        }
    
    @staticmethod
    def save_instructions(instructions):
        """Salva istruzioni su JSON (ma non verranno usate)"""
        Storage.ensure_data_dir()
        with open(INSTRUCTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(instructions, f, indent=2, ensure_ascii=False)