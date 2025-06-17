import streamlit as st
import google.generativeai as genai

if "google" not in st.secrets or "API_KEY" not in st.secrets["google"]:
    st.error("Clé API manquante dans secrets.toml")
    st.stop()

# Config de l'API
genai.configure(api_key=st.secrets.google.API_KEY)

# Prompt système
system_prompt = """lorsque tu reponds soit précis et concis, lors de la première reponse fait un bref résumer et précise sur 
quelle tu travail il faut que tes reponses soient variés pour ne pas avoir l'impression de faire toujours meme chose
et demande si besoin à l'utilisateur de détaillé ta réponse
Tu es un spécialiste de l'animation pour les EHPAD.
Ton objectif : améliorer la motricité et le bien‑être des résidents, timulation cognitive, Maintien de la motricité,
Création de lien social, Amélioration du bien-être émotionnel.
Propose des activités adaptées (PMR inclus)…
souvent pas de budget pour les manifestations
propose des sites avec des activités ludiques sur lesquels je peux m'appuyer et donnes des exemples
leur age varie de 65 ans à 105 ans, pathologies spécifiques fréquentes (Alzheimer, Parkinson, problèmes articulaires, etc)
en général, les residents aime bien la médiation animal.
si la question ne porte pas sur l'animation et le bien être des personnes agées, réponds que tu ne réponds que sur l'animation


"""


# Fonction pour initialiser le chat
def init_chat():
    model = genai.GenerativeModel("gemini-2.0-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": [system_prompt]},
            {
                "role": "model",
                "parts": ["Comment puis-je vous aider aujourdh'hui Gwladys ."],
            },
        ]
    )
    return chat


# Initialisation du chat
if "chat" not in st.session_state:
    st.session_state.chat = init_chat()
    st.session_state.messages = [
        {
            "role": "assistant",
            "text": "Je suis prêt pour t'aider ... 🔎 ",
        }
    ]

# Affichage de la discussion
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Champ de saisie
user_input = st.chat_input(
    "Dis moi ce que tu veux faire pour animer les ptits vieux ... "
)

# Traitement du message
if user_input:
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Obtenir la réponse de Gemini
    response = st.session_state.chat.send_message(user_input)

    # Afficher la réponse du bot
    st.session_state.messages.append({"role": "assistant", "text": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)

# Bouton de réinitialisation en dessous de la zone de texte du chatbot
if st.button("Réinitialiser le ChatBot  🤖", key="reset_button"):
    st.session_state.chat = init_chat()
    st.session_state.messages = [
        {
            "role": "assistant",
            "text": "Comment puis-je vous aider aujourdh'hui Gwladys ? 🔎",
        }
    ]
    st.rerun()
