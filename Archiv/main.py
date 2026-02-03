# main.py
from retriever import retrieve_context
from generator import query_llm

def run_rag():
    query = input("Bitte gib deine Frage ein: ")

    print("\nÄhnliche Dokumente werden gesucht ...")
    context = retrieve_context(query)
    print(context)

    print("\nFrage wird an das LLM (Gemma3:4b) gesendet ...")
    answer = query_llm(query, context)

    print("\n--- Antwort des Systems ---\n")
    print(answer)
    print("\n----------------------------")

if __name__ == "__main__":
    run_rag()
