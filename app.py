import streamlit as st
from retriever import retrieve_context
from generator import query_llm
from auth import register, login


st.set_page_config(page_title="Basketball RAG Chatbot", layout="wide")
st.title("💬 Basketball RAG Chatbot")
st.write("Stelle Fragen zu Basketballregeln – mit Qdrant + Gemma3:4b")


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
            st.success(f"Willkommen {login_user}!")
            
        else:
            st.error("Benutzername oder Passwort falsch")

else:
    # Logout Button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.messages = []
        

    st.write(f"👋 Angemeldet als {st.session_state.user}")





    if "messages" not in st.session_state:
       st.session_state.messages = []



    # Chat Input
    query = st.chat_input("🧠 Stelle deine Frage...")

    if query:
        # User Message speichern
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

    # Chatverlauf anzeigen
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            chat_history = "\n".join(
                f"{m['role']}: {m['content']}"
                for m in st.session_state.messages[-6:]
            )

            retrieval_query = f"""
            Kontext des bisherigen Gesprächs:
            {chat_history}

            Aktuelle Frage:
            {query}
            """



            with st.spinner("🔍 Suche relevante Dokumente..."):
                context = retrieve_context(retrieval_query)

            with st.spinner("💬 Generiere Antwort..."):
                answer = query_llm(query, context)

            st.markdown(answer)

            # Assistant Message speichern
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        # Optional: Kontext anzeigen
        with st.expander("🔎 Kontext aus Qdrant anzeigen"):
            st.text(context)

    