# llm.py
from ollama import chat
from config import LLM_MODEL

def query_llm(query: str, context: str) -> str:
    """
    Sendet eine Anfrage an das Ollama-Modell und gibt die Antwort zurück.
    """
    system_prompt = f"""
    Du sollst Fragen anhand des Kontexts beantworten.
    Gib klare, sachliche und kurze Antworten.
    
    Kontext:
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
