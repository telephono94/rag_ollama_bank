# llm.py
from ollama import chat
from config import LLM_MODEL

def query_llm(query: str, context: str, chat_history: list) -> str:

    system_prompt = f"""
    
    Du bist ein hilfreicher Basketball-Regelassistent.
    
    Wichtige Regeln:
    - Beantworte ausschließlich Fragen zu Basketballregeln.
    - Nutze ausschließlich die bereitgestellten Dokumente als Faktenbasis.
    - Wenn die Frage nicht durch die Fakten aus den Dokumenten beantwortet werden kann, sage ausdrücklich, dass die Informationen in den Dokumenten nicht ausreichen, um die Frage zu beantworten.
    - Erfinde keine Antworten und nutze kein allgemeines Weltwissen.
    - Wenn eine Frage ein anderes Thema (z. B. Fußball) betrifft, sage klar, dass du dazu keine Informationen hast.
    - Erinnerungen dienen nur zum besseren Gesprächsfluss.
    - Wenn Dokumente und Erinnerungen widersprechen, ignoriere die Erinnerungen.
    - Gib klare, sachliche und kurze Antworten.

    Fakten aus Dokumenten:
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
