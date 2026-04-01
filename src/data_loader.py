# src/data_loader.py — Load and chunk Indian knowledge documents
import os
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document


DATA_DIR = Path("./data/raw")


def load_pdf(path: str) -> list[Document]:
    """Load a PDF file and return LangChain documents."""
    loader = PyPDFLoader(path)
    return loader.load()


def load_text(path: str) -> list[Document]:
    """Load a plain text file."""
    loader = TextLoader(path, encoding="utf-8")
    return loader.load()


def chunk_documents(docs: list[Document], chunk_size=500, chunk_overlap=50) -> list[Document]:
    """Split documents into chunks for FAISS."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(docs)


def load_all_domains() -> dict[str, list[Document]]:
    """Load all domain datasets."""
    domains = {}

    # Law
    ipc_path = DATA_DIR / "ipc.pdf"
    if ipc_path.exists():
        domains["law"] = chunk_documents(load_pdf(str(ipc_path)))
        print(f"✅ Law: {len(domains['law'])} chunks")

    # Religion
    gita_path = DATA_DIR / "gita.txt"
    if gita_path.exists():
        domains["religion"] = chunk_documents(load_text(str(gita_path)))
        print(f"✅ Religion: {len(domains['religion'])} chunks")

    # Travel
    travel_path = DATA_DIR / "kolkata_travel.txt"
    if travel_path.exists():
        domains["travel"] = chunk_documents(load_text(str(travel_path)))
        print(f"✅ Travel: {len(domains['travel'])} chunks")

    return domains
