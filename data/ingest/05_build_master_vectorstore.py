# data/ingest/05_build_master_vectorstore.py
# Build master FAISS vectorstore from ALL India data sources

import os, json
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

RAW = Path('data/raw')
FAISS_PATH = 'data/faiss_index'
os.makedirs(FAISS_PATH, exist_ok=True)


def load_json_as_docs(path: str, content_key: str, meta_prefix: str) -> list[Document]:
    """Load a JSON array file and create LangChain documents."""
    docs = []
    try:
        with open(path, encoding='utf-8') as f:
            items = json.load(f)
        for item in items:
            text_parts = [f"{meta_prefix}:"]
            for k, v in item.items():
                if v:
                    text_parts.append(f"{k}: {v}")
            docs.append(Document(
                page_content='\n'.join(text_parts),
                metadata={'source': path, 'type': meta_prefix}
            ))
        print(f'  Loaded {len(docs)} docs from {path}')
    except Exception as e:
        print(f'  Failed {path}: {e}')
    return docs


def build_vectorstore():
    all_docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # PDFs
    for pdf_name in ['ipc.pdf', 'india_tourism_stats_2022.pdf', 'mospi_compendium_2024.pdf']:
        pdf_path = RAW / pdf_name
        if pdf_path.exists():
            try:
                docs = PyPDFLoader(str(pdf_path)).load()
                all_docs += splitter.split_documents(docs)
                print(f'  PDF: {pdf_name} -> {len(docs)} pages')
            except Exception as e:
                print(f'  PDF failed {pdf_name}: {e}')

    # Text files
    for txt_name in [
        'gita.txt', 'ramayana.txt', 'quran_english.txt', 'bible_kjv.txt',
        'wiki_india.txt', 'heritage_religion_wiki.txt', 'indian_law_wiki.txt'
    ]:
        txt_path = RAW / txt_name
        if txt_path.exists():
            try:
                docs = TextLoader(str(txt_path), encoding='utf-8').load()
                all_docs += splitter.split_documents(docs)
                print(f'  TXT: {txt_name} -> {len(docs)} doc(s)')
            except Exception as e:
                print(f'  TXT failed {txt_name}: {e}')

    # JSON structured data
    for json_name, prefix in [
        ('kolkata_hotels.json', 'Hotel'),
        ('tourist_places.json', 'Tourist Place'),
        ('kolkata_routes.json', 'Travel Route')
    ]:
        json_path = RAW / json_name
        if json_path.exists():
            all_docs += load_json_as_docs(str(json_path), 'name', prefix)

    print(f'\nTotal chunks to index: {len(all_docs)}')

    # Build embeddings + FAISS
    print('Building FAISS index (this may take a few minutes)...')
    embeddings = HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    db = FAISS.from_documents(all_docs, embeddings)
    db.save_local(FAISS_PATH)
    print(f'\n✅ FAISS vectorstore saved to {FAISS_PATH}')
    print(f'   Total documents indexed: {len(all_docs)}')

    # Quick test
    test_queries = [
        'Best budget hotel in Kolkata under 2000',
        'What is IPC Section 302?',
        'Things to do near Howrah Bridge',
        'What does Bhagavad Gita say about karma?'
    ]
    print('\nTest queries:')
    for q in test_queries:
        results = db.similarity_search(q, k=1)
        print(f'  Q: {q}')
        print(f'  A: {results[0].page_content[:200]}...\n')


if __name__ == '__main__':
    build_vectorstore()
