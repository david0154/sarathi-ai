# src/vectorstore.py — FAISS vector store management
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from .config import EMBED_MODEL, FAISS_INDEX_PATH
import os


def get_embeddings() -> HuggingFaceEmbeddings:
    """Load SentenceTransformer embeddings."""
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def build_vectorstore(docs: list[Document], save: bool = True) -> FAISS:
    """Build FAISS index from documents."""
    embeddings = get_embeddings()
    db = FAISS.from_documents(docs, embeddings)
    if save:
        os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
        db.save_local(FAISS_INDEX_PATH)
        print(f"✅ FAISS index saved to {FAISS_INDEX_PATH}")
    return db


def load_vectorstore() -> FAISS:
    """Load existing FAISS index."""
    embeddings = get_embeddings()
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings)


def search(db: FAISS, query: str, k: int = 3) -> list[Document]:
    """Semantic search over the vector store."""
    return db.similarity_search(query, k=k)
