import streamlit as st
from retriever import retrieve_context
from generator import query_llm

st.set_page_config(page_title="Basketball RAG Chatbot", layout="wide")
st.title("💬 Basketball RAG Chatbot")
st.write("Stelle Fragen zu Basketballregeln – mit Qdrant + Gemma3:4b")

# Session State initialisieren
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

