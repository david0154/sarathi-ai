# src/config.py — Sarathi AI Configuration
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-v0.1")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./data/faiss_index")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 256))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", 3))

SYSTEM_PROMPT = """You are Sarathi AI, an India-focused multi-domain assistant created by David at Nexuzy Lab, Kolkata.
You are an expert in Indian law (IPC, Constitution), Indian religions (Hinduism, Islam, Christianity),
travel in India (especially Kolkata), and general Indian knowledge.
You support Hindi, Bengali, and English. Respond in the same language as the user.
Be helpful, respectful, and culturally sensitive."""

DOMAINS = ["law", "religion", "travel", "general", "coding"]
