from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL_NAME

loader1 = PyPDFLoader("./knowledge/Projektbericht_Customer_Health_Check.pdf")
loader2 = PyPDFLoader("./knowledge/S4.pdf")
documents = loader1.load() + loader2.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Load the embedding model 
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

qdrant = QdrantVectorStore.from_documents(
    documents=texts,
    embedding=embeddings,
    url=QDRANT_URL,
    prefer_grpc=False,
    collection_name=COLLECTION_NAME
)

print("Vector DB Successfully Created!")