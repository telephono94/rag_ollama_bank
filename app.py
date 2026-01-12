import streamlit as st
from retriever import retrieve_context
from generator import query_llm
from auth import register, login
from chat_db import init_db, save_message, load_chat, clear_chat

init_db()


st.set_page_config(page_title="Basketball RAG Chatbot", layout="wide")
st.title("🏀 Basketball RAG Chatbot")
st.write("Stelle Fragen zu Basketballregeln – mit Qdrant als Datenbank + Gemma3:4b als LLM")


# Session State für Login + Chat
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔐 Login / Registrierung
if not st.session_state.logged_in:
    st.subheader("Registrieren")
    reg_user = st.text_input("Username (neu)", key="reg_user")
    reg_pass = st.text_input("Passwort", type="password", key="reg_pass")
    if st.button("Registrieren"):
        success, msg = register(reg_user, reg_pass)
        if success:
            st.success(msg)
        else:
            st.warning(msg)

    st.subheader("Login")
    login_user = st.text_input("Username", key="login_user")
    login_pass = st.text_input("Passwort", type="password", key="login_pass")
    if st.button("Login"):
        if login(login_user, login_pass):
            st.session_state.logged_in = True
            st.session_state.user = login_user
            st.session_state.messages = load_chat(login_user)
            st.success(f"Willkommen {login_user}!")
            st.rerun()
            
        else:
            st.error("Benutzername oder Passwort falsch")

else:
    
    if "messages" not in st.session_state:
       st.session_state.messages = load_chat(st.session_state.user)

    if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()

    
    if st.button("🗑️ Chat löschen"):
        clear_chat(st.session_state.user)
        st.session_state.messages = []
        st.rerun()
        

    st.write(f"👋 Angemeldet als {st.session_state.user}")

    

    

    # Chatverlauf anzeigen
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    
    
    
    
    # Chat Input
    query = st.chat_input("🧠 Stelle eine Frage zu Basketballregeln...")

    if query:

        with st.chat_message("user"):
            st.markdown(query)

        chat_history = [
                m for m in st.session_state.messages[-6:]
                if m["role"] in ("user", "assistant")
            ]  


        # User Message speichern
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        save_message(st.session_state.user, "user", query)

        with st.chat_message("assistant"):            

            with st.spinner("🔍 Suche relevante Dokumente..."):
                context = retrieve_context(query)

            with st.spinner("💬 Generiere Antwort..."):
                answer = query_llm(query, context, chat_history)

            st.markdown(answer)

            # Assistant Message speichern
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            save_message(st.session_state.user, "assistant", answer)
  
            # Optional: Kontext anzeigen
            with st.expander("🔎 Kontext aus Qdrant anzeigen"):
                st.text(context)
