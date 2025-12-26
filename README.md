# AI Chatbot - Streamlit Interface

Interfaccia chat con supporto conversazioni multiple e configurazione agente personalizzata.

## Setup

1. **Clone repository**
   ```bash
   git clone <your-repo>
   cd chatbot-app
   ```

2. **Crea virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Installa dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura API**
   ```bash
   cp .env.example .env
   # Modifica .env con la tua API key
   ```

5. **Avvia app**
   ```bash
   streamlit run app.py
   ```

## Configurazione

Modifica `.env`:
```env
API_KEY=your_api_key_here
API_BASE_URL=https://api.together.xyz/v1
MODEL_NAME=meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo
```

## Features

- ✅ Conversazioni multiple con salvataggio automatico
- ✅ System prompt personalizzabile
- ✅ Regole specifiche per domande ricorrenti
- ✅ Streaming responses
- ✅ Persistenza dati (JSON locale)

## Struttura

- `app.py` - App principale Streamlit
- `config.py` - Configurazione e costanti
- `utils/storage.py` - Gestione salvataggio/caricamento dati
- `data/` - File JSON con conversazioni e istruzioni

## Licenza

MIT
