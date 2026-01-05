# RAG Ollama Berater

Ein einfaches Retrieval-Augmented-Generation (RAG) System mit:
- Qdrant als Vektor-Datenbank
- HuggingFace BGE Embeddings
- Ollama (Gemma3:4b) als LLM

## Start

1. Virtuelle Umgebung erstellen und starten:
   ```bash 
   python -m venv .venv

   .venv\Scripts\Activate.ps1

2. Notwendigen Python-Pakete installieren
   ```bash
   pip install -r requirements.txt

3. Docker Desktop öffnen, damit die Docker Engine automatisch startet

4. Qdrant starten:
   ```bash
   docker compose up
Öffne Qdrant unter localhost:6333/dashboard


5. Vektordatenbank erstellen:
   ```bash
   python ingest.py

6. App starten:
   ```bash
   streamlit run app.py