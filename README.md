# RAG Ollama Berater

Ein einfaches Retrieval-Augmented-Generation (RAG) System mit:
- Qdrant als Vektor-Datenbank
- HuggingFace BGE Embeddings
- Ollama (Gemma3:4b) als LLM

## Start

1. Qdrant starten:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant



Führe "python main.py" aus

oder "streamlit run app.py" für eine Benutzeroberfläche 