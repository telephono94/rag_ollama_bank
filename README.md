# RAG Ollama Berater

Ein einfaches Retrieval-Augmented-Generation (RAG) System mit:
- Qdrant als Vektor-Datenbank
- HuggingFace BGE Embeddings
- Ollama (Gemma3:4b) als LLM

## Start

1. Qdrant starten:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant


2. App starten:
```bash
streamlit run app.py