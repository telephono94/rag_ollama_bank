# retriever.py
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL_NAME
from langchain_huggingface import HuggingFaceEmbeddings

def get_vectorstore():
    """
    Erstellt den Qdrant-Vektorstore mit HuggingFace-Embeddings.
    """
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    client = QdrantClient(url=QDRANT_URL, prefer_grpc=False)

    db = QdrantVectorStore(client=client, embedding=embeddings, collection_name=COLLECTION_NAME)
    return db


def retrieve_context(query: str, k: int = 5) -> str:
    """
    Führt eine semantische Suche in der Qdrant-Collection durch und gibt den kombinierten Kontext zurück.
    """
    db = get_vectorstore()
    docs = db.similarity_search_with_score(query=query, k=k)

    context_text = "\n\n".join(
        [f"- (Score: {score:.3f}) {doc.page_content}" for doc, score in docs]
    )
    return context_text
