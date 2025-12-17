import streamlit as st
from retriever import retrieve_context
from generator import query_llm

st.set_page_config(page_title="💼 Bankberater RAG", page_icon="🏦", layout="wide")

st.title("💬 KI-Berater (RAG-System mit Ollama)")
st.write("Stelle eine Frage zum Customer Health Check. Das System nutzt Qdrant + Gemma3:4b zur Beantwortung.")

query = st.text_input("🧠 Deine Frage:", placeholder="z. B. Sind ländliche oder städtische Kunden wertvoller?")

if st.button("Antwort generieren") and query:
    with st.spinner("🔍 Suche relevante Dokumente..."):
        context = retrieve_context(query)

    with st.spinner("💬 Generiere Antwort mit Gemma3:4b..."):
        answer = query_llm(query, context)

    st.subheader("Antwort:")
    st.write(answer)

    with st.expander("🔎 Kontext aus Qdrant anzeigen"):
        st.text(context)
