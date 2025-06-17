import os
import streamlit as st
from google import genai

# impor


# ───────── 1. Récupération sécurisée de la clé API ─────────
def get_api_key() -> str | None:
    """
    Recherche la clé dans l'ordre de priorité suivant :
    1. st.secrets["GOOGLE_API_KEY"] (fichier secrets.toml ou réglage Streamlit Cloud)
    2. Variable d'environnement GOOGLE_API_KEY
    """
    if "GOOGLE_API_KEY" in st.secrets:  # priorité 1
        return st.secrets["GOOGLE_API_KEY"]


API_KEY = get_api_key()

if not API_KEY:
    st.error(
        "Clé GOOGLE_API_KEY manquante. "
        "Ajoutez‑la dans st.secrets ou comme variable d’environnement."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)  # Client Gemini

# ───────── 2. Prompt système & création du chat ──────────
SYSTEM_PROMPT = (
    "Tu es un spécialiste de l'animation pour les EHPAD. "
    "Ton objectif : améliorer la motricité et le bien‑être des résidents. "
    "Propose des activités adaptées (PMR inclus)…"
)


def init_chat():
    history = [
        {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]},
        {
            "role": "model",
            "parts": [{"text": "Compris ! Posez votre première question."}],
        },
    ]
    return client.chats.create(model="gemini-2.0-flash-001", history=history)


# ───────── 3. Initialisation de l’état Streamlit ─────────
if "chat" not in st.session_state:
    st.session_state.chat = init_chat()
    st.session_state.messages = [
        {
            "role": "assistant",
            "text": "Bonjour ! Comment puis‑je vous aider pour l’animation en EHPAD ?",
        },
    ]

# ───────── 4. Affichage de l’historique ────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# ───────── 5. Entrée utilisateur + streaming ───────────
user_input = st.chat_input("Posez votre question…")

if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response_stream = st.session_state.chat.send_message_stream(user_input)
    partial = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        for chunk in response_stream:
            partial += chunk.text
            placeholder.markdown(partial + "▌")
    st.session_state.messages.append({"role": "assistant", "text": partial})

# ───────── 6. Réinitialisation de la session ───────────
if st.button("🔄 Réinitialiser le bot"):
    st.session_state.chat = init_chat()
    st.session_state.messages = [
        {"role": "assistant", "text": "Bot réinitialisé. Posez une nouvelle question."},
    ]
