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
        """Carica istruzioni: config.py (backend) + JSON (frontend extra)"""
        Storage.ensure_data_dir()
        
        # Carica regole EXTRA dal JSON (create dall'interfaccia)
        extra_rules = []
        if os.path.exists(INSTRUCTIONS_FILE):
            with open(INSTRUCTIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                extra_rules = data.get("custom_rules", [])
        
        # Ritorna: regole backend + regole frontend EXTRA
        return {
            "system_prompt": DEFAULT_SYSTEM_PROMPT,
            "backend_rules": DEFAULT_CUSTOM_RULES,  # Invisibili nell'interfaccia
            "custom_rules": extra_rules  # Visibili e modificabili
        }
    
    @staticmethod
    def save_instructions(instructions):
        """Salva solo le regole EXTRA (non quelle backend)"""
        Storage.ensure_data_dir()
        
        # Salva solo custom_rules (quelle aggiunte dall'interfaccia)
        to_save = {
            "system_prompt": instructions["system_prompt"],
            "custom_rules": instructions.get("custom_rules", [])
        }
        
        with open(INSTRUCTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(to_save, f, indent=2, ensure_ascii=False)