"""
Sarathi AI — India Data Cleaning Pipeline
Developer: David | Nexuzy Lab, Kolkata

Cleans raw text, PDFs, JSON, and CSV collected from India public datasets.
Outputs cleaned JSONL ready for FAISS + RAG ingestion.

Usage:
    python training/data_cleaning.py
"""

import os
import re
import json
import csv
from pathlib import Path
from typing import List

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/cleaned")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------
# CORE TEXT CLEANING
# -----------------------------------------------

def clean_text(text: str) -> str:
    """Normalize whitespace, remove junk characters, keep ASCII+Hindi+Bengali."""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping word chunks for RAG ingestion."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i: i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


# -----------------------------------------------
# EXTRACTORS per file type
# -----------------------------------------------

def extract_pdf_text(path: str) -> str:
    if PdfReader is None:
        raise ImportError("Install pypdf: pip install pypdf")
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return clean_text(" ".join(pages))


def extract_txt_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return clean_text(f.read())


def extract_json_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        parts = [" ".join(str(v) for v in item.values()) if isinstance(item, dict) else str(item) for item in data]
        return clean_text(" ".join(parts))
    return clean_text(json.dumps(data, ensure_ascii=False))


def extract_csv_text(path: str) -> str:
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            rows.append(" ".join(str(v) for v in row.values()))
    return clean_text(" ".join(rows))


EXTRACTORS = {
    ".pdf": extract_pdf_text,
    ".txt": extract_txt_text,
    ".json": extract_json_text,
    ".csv": extract_csv_text,
}


# -----------------------------------------------
# AUTO-TAGGER
# -----------------------------------------------

def tag_category(filename: str) -> str:
    name = filename.lower()
    mapping = {
        "law":      ["ipc", "constitution", "law", "legal"],
        "tourism":  ["tourism", "hotel", "kolkata", "west_bengal", "travel", "place"],
        "weather":  ["weather", "imd", "climate", "temperature"],
        "police":   ["police", "crime", "ncrb"],
        "election": ["election", "politics", "vote"],
        "economy":  ["economy", "rbi", "gdp", "finance"],
        "sports":   ["sport", "cricket", "ipl", "olympic"],
        "cyber":    ["cyber", "cert", "security"],
        "religion": ["gita", "quran", "ramayana", "bible", "religion"],
        "social":   ["reddit", "gdelt", "social", "news"],
        "maps":     ["map", "city", "state", "district", "location", "coord"],
    }
    for category, keywords in mapping.items():
        if any(k in name for k in keywords):
            return category
    return "general"


# -----------------------------------------------
# MAIN PIPELINE
# -----------------------------------------------

def process_all(
    raw_dir: Path = RAW_DIR,
    out_dir: Path = OUT_DIR,
    chunk_size: int = 500,
    overlap: int = 50,
):
    records = []
    files = [f for f in raw_dir.rglob("*") if f.is_file()]
    print(f"Found {len(files)} files in {raw_dir}")

    for fp in files:
        ext = fp.suffix.lower()
        extractor = EXTRACTORS.get(ext)
        if extractor is None:
            continue
        print(f"  Processing {fp.name} ({ext})...")
        try:
            raw_text = extractor(str(fp))
            chunks = chunk_text(raw_text, chunk_size, overlap)
            category = tag_category(fp.name)
            for i, chunk in enumerate(chunks):
                records.append({
                    "id": f"{fp.stem}_chunk_{i}",
                    "source": fp.name,
                    "category": category,
                    "text": chunk,
                    "char_count": len(chunk),
                })
            print(f"    OK  {len(chunks)} chunks [{category}]")
        except Exception as e:
            print(f"    FAIL {fp.name}: {e}")

    out_path = out_dir / "sarathi_cleaned.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"\nDone — {len(records)} chunks saved to {out_path}")
    return records


if __name__ == "__main__":
    process_all()
