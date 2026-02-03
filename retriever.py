# retriever.py
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL_NAME
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder

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

"""
def retrieve_context(query: str, k: int = 30) -> str:
    db = get_vectorstore()
    retrieved = db.similarity_search_with_score(query=query, k=k)

    documents = [doc for doc, _ in retrieved]

    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    pairs = [(query, doc.page_content) for doc in documents]
    rerank_scores = reranker.predict(pairs)

    reranked = sorted(
        zip(documents, rerank_scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_docs = [doc for doc, _ in reranked[:10]]

    return "\n\n".join(doc.page_content for doc in top_docs)
"""

def retrieve_context(query: str, k: int = 30) -> str:
    db = get_vectorstore()
    retrieved = db.similarity_search_with_score(query=query, k=k)
    # retrieved: List[(Document, retrieval_score)]

    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    # Query-Dokument-Paare für den Reranker
    pairs = [(query, doc.page_content) for doc, _ in retrieved]
    rerank_scores = reranker.predict(pairs)

    # Alles zusammenführen
    combined = [
        {
            "doc": doc,
            "retrieval_score": retrieval_score,
            "rerank_score": rerank_score,
        }
        for (doc, retrieval_score), rerank_score in zip(retrieved, rerank_scores)
    ]

    # Nach Rerank-Score sortieren
    combined = sorted(
        combined,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # Top-N auswählen
    top_chunks = combined[:10]

    # Kontext mit Scores formatieren
    context = "\n\n".join(
        f"""[Chunk {i+1}]
    Retrieval-Score: {chunk['retrieval_score']:.4f}
    Rerank-Score: {chunk['rerank_score']:.4f}

    {chunk['doc'].page_content}
    """
        for i, chunk in enumerate(top_chunks)
    )

    return context
