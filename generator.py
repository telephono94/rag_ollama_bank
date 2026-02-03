# llm.py
from ollama import chat
from config import LLM_MODEL

def query_llm(query: str, context: str, chat_history: list) -> str:

    system_prompt = f"""
    
    Du bist ein hilfreicher Basketball-Regelassistent.
    
    ANTWORTREGELN:
    1. Antworte nur auf Basis der unten stehenden Dokumente.
    2. Wenn die Dokumente die Frage nicht abdecken, antworte: "Die bereitgestellten Dokumente enthalten keine Informationen zu dieser Frage."
    3. Keine Erfindungen, kein Weltwissen.
    4. Antworten, die nicht aus den Dokumenten stammen, sind verboten.


    Dokumente:
    {context}
    """

    response = chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *chat_history,
            {"role": "user", "content": query}
        ]
    )
    return response["message"]["content"].strip()
