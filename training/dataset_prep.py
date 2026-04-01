# training/dataset_prep.py — Prepare Indian-specific chat dataset
from datasets import load_dataset, Dataset, concatenate_datasets
from transformers import AutoTokenizer
from src.config import MODEL_NAME, SYSTEM_PROMPT
import json


def load_indian_law_qa() -> Dataset:
    """Create a small Indian law QA dataset manually."""
    examples = [
        {"question": "What is IPC Section 302?", "answer": "IPC Section 302 deals with punishment for murder. The punishment is death or life imprisonment plus fine."},
        {"question": "What is Article 21 of the Indian Constitution?", "answer": "Article 21 guarantees the right to life and personal liberty. No person shall be deprived of his life except according to procedure established by law."},
        {"question": "What is IPC Section 420?", "answer": "IPC Section 420 deals with cheating and dishonestly inducing delivery of property. Punishment is up to 7 years imprisonment."},
        {"question": "What is the Right to Information Act?", "answer": "The RTI Act 2005 grants Indian citizens the right to access information held by public authorities. It promotes transparency and accountability."},
    ]
    texts = []
    for ex in examples:
        text = f"{SYSTEM_PROMPT}\n\nUser: {ex['question']}\nSarathi: {ex['answer']}"
        texts.append({"text": text})
    return Dataset.from_list(texts)


def load_kolkata_travel_qa() -> Dataset:
    """Create a Kolkata travel QA dataset."""
    examples = [
        {"question": "Best budget hotels in Kolkata?", "answer": "Some top budget hotels in Kolkata include Broadway Hotel (Park Street area), Hotel Centrum, and Lytton Hotel — all under ₹2000/night."},
        {"question": "How to reach Kolkata airport from city center?", "answer": "You can reach Kolkata's Netaji Subhas Chandra Bose Airport via metro (Blue Line to Noapara, then Airport metro), taxi (Ola/Uber ~₹500-700), or AC bus routes."},
        {"question": "What are the must-visit places in Kolkata?", "answer": "Top places: Victoria Memorial, Howrah Bridge, Dakshineswar Temple, College Street, Park Street, New Market, Sundarbans (day trip)."},
    ]
    texts = []
    for ex in examples:
        text = f"{SYSTEM_PROMPT}\n\nUser: {ex['question']}\nSarathi: {ex['answer']}"
        texts.append({"text": text})
    return Dataset.from_list(texts)


def build_combined_dataset() -> Dataset:
    """Combine all domain datasets + general dialog."""
    # General dialog
    general = load_dataset("daily_dialog", split="train[:5000]")
    general_texts = []
    for ex in general:
        dialog = ex.get("dialog", [])
        text = f"{SYSTEM_PROMPT}\n\n"
        for i, turn in enumerate(dialog[:4]):
            role = "User" if i % 2 == 0 else "Sarathi"
            text += f"{role}: {turn.strip()}\n"
        general_texts.append({"text": text})
    general_dataset = Dataset.from_list(general_texts)

    # Domain-specific
    law_dataset = load_indian_law_qa()
    travel_dataset = load_kolkata_travel_qa()

    # Combine
    combined = concatenate_datasets([general_dataset, law_dataset, travel_dataset])
    combined = combined.shuffle(seed=42)
    print(f"✅ Combined dataset: {len(combined)} samples")
    return combined


if __name__ == "__main__":
    ds = build_combined_dataset()
    ds.save_to_disk("./data/processed/sarathi_train_dataset")
    print("✅ Dataset saved!")
