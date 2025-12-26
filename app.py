import streamlit as st
from groq import Groq
from datetime import datetime
from utils import Storage
import config

# Configurazione pagina
st.set_page_config(page_title="Chat Assistant", layout="wide")

# Inizializza client OpenAI
@st.cache_resource
def get_client():
    return Groq(api_key=config.API_KEY)

# Inizializza stato
if "conversations" not in st.session_state:
    st.session_state.conversations = Storage.load_conversations()

if "instructions" not in st.session_state:
    st.session_state.instructions = Storage.load_instructions()

if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = None

if "client" not in st.session_state:
    st.session_state.client = get_client()

# Funzioni
def new_conversation():
    conv_id = f"conv_{len(st.session_state.conversations) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.conversations[conv_id] = {
        "messages": [],
        "title": f"Chat {len(st.session_state.conversations) + 1}",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    st.session_state.current_conv_id = conv_id
    Storage.save_conversations(st.session_state.conversations)

def build_system_message():
    base = st.session_state.instructions["system_prompt"]
    rules = st.session_state.instructions["custom_rules"]
    
    if rules:
        rules_text = "\n\nRegole specifiche:\n" + "\n".join(
            [f"- {r['question']}: {r['answer']}" for r in rules]
        )
        return base + rules_text
    return base

# SIDEBAR
with st.sidebar:
    st.title("💬 Chattami")
    
    tab1, tab2 = st.tabs(["Conversazioni", "⚙️ Istruzioni"])
    
    # TAB CONVERSAZIONI
    with tab1:
        if st.button("➕ Nuova Chat", use_container_width=True):
            new_conversation()
            st.rerun()
        
        st.divider()
        
        for conv_id, conv_data in reversed(list(st.session_state.conversations.items())):
            is_current = conv_id == st.session_state.current_conv_id
            
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    f"{'🟢' if is_current else '⚪'} {conv_data['title']}", 
                    key=f"btn_{conv_id}",
                    use_container_width=True
                ):
                    st.session_state.current_conv_id = conv_id
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}"):
                    del st.session_state.conversations[conv_id]
                    if st.session_state.current_conv_id == conv_id:
                        st.session_state.current_conv_id = None
                    Storage.save_conversations(st.session_state.conversations)
                    st.rerun()
    
    # TAB ISTRUZIONI
    with tab2:
        st.subheader("System Prompt Base")
        new_prompt = st.text_area(
            "Comportamento generale",
            value=st.session_state.instructions["system_prompt"],
            height=150
        )
        if st.button("Salva Prompt"):
            st.session_state.instructions["system_prompt"] = new_prompt
            Storage.save_instructions(st.session_state.instructions)
            st.success("✓ Salvato")
        
        st.divider()
        st.subheader("Risposte Specifiche")
        
        with st.expander("➕ Aggiungi Regola"):
            new_q = st.text_input("Domanda/Trigger")
            new_a = st.text_area("Come rispondere")
            if st.button("Aggiungi"):
                if new_q and new_a:
                    st.session_state.instructions["custom_rules"].append({
                        "question": new_q,
                        "answer": new_a
                    })
                    Storage.save_instructions(st.session_state.instructions)
                    st.rerun()
        
        for idx, rule in enumerate(st.session_state.instructions["custom_rules"]):
            with st.expander(f"📌 {rule['question'][:30]}..."):
                st.write(f"**Q:** {rule['question']}")
                st.write(f"**A:** {rule['answer']}")
                if st.button("🗑️ Elimina", key=f"del_rule_{idx}"):
                    st.session_state.instructions["custom_rules"].pop(idx)
                    Storage.save_instructions(st.session_state.instructions)
                    st.rerun()

# MAIN AREA
if st.session_state.current_conv_id is None:
    st.title("Benvenuto! 👋")
    st.write("Crea una nuova conversazione per iniziare.")
    if st.button("Inizia una nuova chat"):
        new_conversation()
        st.rerun()
else:
    current_conv = st.session_state.conversations[st.session_state.current_conv_id]
    
    new_title = st.text_input(
        "Titolo",
        value=current_conv["title"],
        label_visibility="collapsed"
    )
    if new_title != current_conv["title"]:
        current_conv["title"] = new_title
        Storage.save_conversations(st.session_state.conversations)
    
    st.divider()
    
    for message in current_conv["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Scrivi un messaggio..."):
        current_conv["messages"].append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            messages = [
                {"role": "system", "content": build_system_message()}
            ] + current_conv["messages"]
            
            stream = st.session_state.client.chat.completions.create(
                model=config.MODEL_NAME,  # usa config invece che "model"
                messages=messages,
                stream=True,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
)
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        current_conv["messages"].append({"role": "assistant", "content": full_response})
        Storage.save_conversations(st.session_state.conversations)
        st.rerun()
