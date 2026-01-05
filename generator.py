# llm.py
from ollama import chat
from config import LLM_MODEL

def query_llm(query: str, context: str, chat_history: str = "") -> str:
    
    system_prompt = f"""
    
    Du bist ein hilfreicher Basketball-Regelassistent.
    
    Wichtige Regeln:
    - Du sollst Fragen anhand der Fakten aus den Dokumenten beantworten.
    - Erinnerungen dienen nur zum besseren Gesprächsfluss.
    - Wenn Dokumente und Erinnerungen widersprechen, ignoriere die Erinnerungen.
    -Gib klare, sachliche und kurze Antworten.

    Relevante Erinnerungen aus dem Gespräch:
    {chat_history}
    
    Fakten aus Dokumenten:
    {context}
    """

    response = chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    return response["message"]["content"].strip()
