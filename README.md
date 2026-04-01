# 🇮🇳 Sarathi AI — India-Focused Multi-Domain Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Developer-David-teal?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Org-Nexuzy%20Lab-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Location-Kolkata%2C%20India-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Model-Mistral%207B-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Framework-LangChain%20%2B%20RAG-green?style=for-the-badge" />
</p>

> **Sarathi AI** is an India-focused, multi-domain conversational assistant built by David @ Nexuzy Lab, Kolkata.  
> It combines RAG (Retrieval-Augmented Generation), QLoRA fine-tuning, and multilingual support for Law, Religion, Travel, General Knowledge, and Coding.

---

## 📌 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Google Colab Training Guide](#google-colab-training-guide)
- [Data Sources](#data-sources)
- [RAG Pipeline](#rag-pipeline)
- [Fine-Tuning with QLoRA](#fine-tuning-with-qlora)
- [Multilingual Support](#multilingual-support)
- [Evaluation & Testing](#evaluation--testing)
- [Deploying to Hugging Face](#deploying-to-hugging-face)
- [Roadmap](#roadmap)
- [License](#license)

---

## Architecture Overview

```
User Input (Hindi / Bengali / English)
        │
        ▼
┌─────────────────────────────────────┐
│         Sarathi AI Core             │
│   (Mistral 7B / LLaMA 3 — 4-bit)   │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│       Router Layer (LangChain)      │
├─────────────┬───────────────────────┤
│  Law DB     │  Religion DB          │
│  (IPC,      │  (Gita, Quran,        │
│  Const.)    │   Bible…)             │
├─────────────┼───────────────────────┤
│  Travel DB  │  General Knowledge    │
│  (Kolkata   │  (Wikipedia India,    │
│  Hotels…)   │   AI4Bharat)          │
└─────────────┴───────────────────────┘
        │
        ▼
┌──────────────────────┐
│  FAISS Vector Search │
│  (Semantic Retrieval)│
└──────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│  Relevant Context → LLM Prompt│
│  → Final Human-Like Answer    │
└───────────────────────────────┘
```

**This = RAG + Fine-tuned LLM + Domain Router + Multilingual NLP**

---

## Features

| Domain | Capability |
|---|---|
| ⚖️ Law | IPC sections, Indian Constitution, Supreme Court Q&A |
| 🛕 Religion | Bhagavad Gita, Quran, Bible — comparative insights |
| 🏨 Travel | Kolkata hotels, routes, local tips |
| 🌐 General | Wikipedia India, current affairs (AI4Bharat) |
| 💻 Coding | Python, Kotlin, JS code generation & explanation |
| 🗣️ Language | Hindi, Bengali, English (multilingual) |
| 👁️ Vision | Vision-ready architecture (future: image input) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| 🧠 Brain | Mistral 7B v0.1 / LLaMA 3 (4-bit QLoRA) |
| 🗄️ Memory / Vector DB | FAISS (CPU) |
| 🔁 Control / Routing | LangChain |
| 🔢 Embeddings | `all-MiniLM-L6-v2` (SentenceTransformers) |
| 🏋️ Training | PEFT (LoRA / QLoRA) via Hugging Face |
| 📚 Data | AI4Bharat, Govt India Code, Project Gutenberg |
| 🚀 Deploy | Hugging Face Hub + Your Servers |
| 🖥️ Training Platform | Google Colab (T4 / A100) |

---

## Project Structure

```
sarathi-ai/
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   ├── raw/
│   │   ├── ipc.pdf                  # Indian Penal Code
│   │   ├── gita.txt                 # Bhagavad Gita
│   │   └── kolkata_travel.txt       # Travel data
│   └── processed/
│       └── chunks/                  # Chunked text for FAISS
│
├── notebooks/
│   ├── 01_data_collection.ipynb     # Download & preprocess data
│   ├── 02_build_vectorstore.ipynb   # FAISS index creation
│   ├── 03_qlora_finetuning.ipynb    # QLoRA training notebook
│   └── 04_evaluation.ipynb          # BLEU / F1 evaluation
│
├── src/
│   ├── config.py                    # Model & path configs
│   ├── data_loader.py               # Load + chunk documents
│   ├── embeddings.py                # Sentence transformer embeddings
│   ├── vectorstore.py               # FAISS build + query
│   ├── router.py                    # LangChain domain router
│   ├── model.py                     # Load Mistral 4-bit
│   ├── pipeline.py                  # RAG pipeline end-to-end
│   └── evaluate.py                  # Evaluation metrics
│
├── training/
│   ├── qlora_config.py              # LoRA hyperparameters
│   ├── train.py                     # Training script
│   └── dataset_prep.py             # Chat dataset formatting
│
└── app/
    ├── app.py                       # Gradio / FastAPI demo
    └── templates/
        └── index.html
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- CUDA GPU (or Google Colab)
- Hugging Face account (for Mistral gated model)

### 1. Clone the Repository

```bash
git clone https://github.com/david0154/sarathi-ai.git
cd sarathi-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your HuggingFace token
```

---

## Google Colab Training Guide

> ✅ **Recommended: Start here if you have no local GPU.**

### Step 1 — Open a New Colab Notebook

Go to [colab.research.google.com](https://colab.research.google.com) → New Notebook → Runtime → Change runtime type → **GPU (T4 or A100)**

### Step 2 — Install Dependencies

```python
!pip install transformers datasets accelerate peft bitsandbytes -q
!pip install langchain faiss-cpu sentence-transformers -q
!pip install huggingface_hub wikipedia pypdf -q
```

### Step 3 — Login to Hugging Face

```python
from huggingface_hub import login
login()  # Enter your HF token when prompted
# Get token at: https://huggingface.co/settings/tokens
```

### Step 4 — Download Indian Datasets

```python
# Indian Penal Code PDF
!wget https://legislative.gov.in/sites/default/files/A1860-45.pdf -O ipc.pdf

# Bhagavad Gita (Project Gutenberg)
!wget https://www.gutenberg.org/files/54868/54868-0.txt -O gita.txt

# Wikipedia India data
import wikipedia
wiki_data = wikipedia.page("Kolkata").content
with open("kolkata.txt", "w") as f:
    f.write(wiki_data)

print("✅ Data downloaded!")
```

### Step 5 — Load Base Model (Mistral 7B in 4-bit)

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

model_name = "mistralai/Mistral-7B-v0.1"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

print("✅ Model loaded!")
```

### Step 6 — Build FAISS Vector Store

```python
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Load your documents
with open("gita.txt", "r") as f:
    gita_text = f.read()

# Chunk documents
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents([gita_text, wiki_data])

# Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

# Save index
db.save_local("faiss_index")
print(f"✅ Vector store built with {len(docs)} chunks!")
```

### Step 7 — RAG Query (Test Before Training)

```python
def sarathi_answer(query: str) -> str:
    # Retrieve context
    results = db.similarity_search(query, k=3)
    context = "\n".join([r.page_content for r in results])

    # Build prompt
    prompt = f"""You are Sarathi AI, an India-focused assistant made by David at Nexuzy Lab, Kolkata.
Use the following context to answer the question in a helpful, friendly way.

Context:
{context}

Question: {query}
Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("Answer:")[-1].strip()

# Test it!
print(sarathi_answer("What is Kolkata famous for?"))
```

### Step 8 — QLoRA Fine-Tuning

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq
from datasets import load_dataset

# Prepare model for QLoRA
model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Expected: ~0.1% of total parameters — very efficient!

# Load chat dataset
dataset = load_dataset("daily_dialog", split="train[:5000]")

def format_chat(example):
    conversation = example["dialog"]
    text = ""
    for i, turn in enumerate(conversation[:4]):
        role = "User" if i % 2 == 0 else "Sarathi"
        text += f"{role}: {turn}\n"
    return {"text": text}

formatted = dataset.map(format_chat)

def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

tokenized = formatted.map(tokenize, batched=True)

training_args = TrainingArguments(
    output_dir="./sarathi-qlora",
    num_train_epochs=2,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=50,
    save_steps=500,
    warmup_steps=100,
    lr_scheduler_type="cosine",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=DataCollatorForSeq2Seq(tokenizer, pad_to_multiple_of=8)
)

print("🚀 Starting training...")
trainer.train()
print("✅ Training complete!")
```

### Step 9 — Save & Upload to Hugging Face

```python
model.save_pretrained("sarathi-ai-merged")
tokenizer.save_pretrained("sarathi-ai-merged")

model.push_to_hub("david0154/Sarathi-AI")
tokenizer.push_to_hub("david0154/Sarathi-AI")
print("✅ Model pushed to HuggingFace Hub!")
```

---

## Data Sources

### ⚖️ Law Data
| Source | URL | Format |
|---|---|---|
| Indian Penal Code | `legislative.gov.in` | PDF |
| Indian Constitution | `legislative.gov.in` | PDF |
| Supreme Court Judgments | `sci.gov.in` | PDF |

### 🛕 Religious Data
| Source | URL | Format |
|---|---|---|
| Bhagavad Gita | Project Gutenberg #54868 | TXT |
| Quran English | Project Gutenberg | TXT |
| Bible KJV | Project Gutenberg | TXT |

### 🏨 Travel Data
| Source | Method | Notes |
|---|---|---|
| Kolkata Hotels | Wikipedia / Manual | CSV |
| Google Maps API | REST API | Later integration |
| MakeMyTrip | Scraping (legal check) | JSON |

### 🌐 General Knowledge
| Source | Method |
|---|---|
| Wikipedia India | `wikipedia` Python library |
| AI4Bharat datasets | HuggingFace Datasets |
| IndicNLP Corpus | GitHub |

---

## RAG Pipeline

```
User Query
    │
    ▼
SentenceTransformer Embedding (all-MiniLM-L6-v2)
    │
    ▼
FAISS Similarity Search (top-k=3)
    │
    ▼
Context Chunks Retrieved
    │
    ▼
Prompt Template (System + Context + Query)
    │
    ▼
Mistral 7B generates final answer
```

The key advantage: The LLM never hallucinates Indian law / religious texts — it always draws from verified, chunked documents.

---

## Fine-Tuning with QLoRA

QLoRA dramatically reduces VRAM — train a 7B model on a **free T4 Colab GPU (16GB)**.

```
Full fine-tune:  7B params × 4 bytes = ~28GB VRAM ❌
QLoRA (4-bit):   7B params × 0.5 bytes + LoRA adapters ≈ ~6GB VRAM ✅
```

**Recommended hyperparameters:**

| Param | Value | Reason |
|---|---|---|
| `r` | 8 | Rank — balance expressiveness vs. size |
| `lora_alpha` | 16 | Scale factor (2×r is standard) |
| `lora_dropout` | 0.05 | Light regularization |
| `batch_size` | 2 | T4 safe batch size |
| `grad_accum` | 4 | Effective batch = 8 |
| `lr` | 2e-4 | Standard QLoRA LR |
| `epochs` | 2-3 | Enough for domain adaptation |

---

## Multilingual Support

Sarathi AI supports Hindi, Bengali, and English natively.

**Strategy 1 — Mixed dataset training:**
```python
from datasets import concatenate_datasets, load_dataset

english_data = load_dataset("daily_dialog", split="train[:2000]")
hindi_data = load_dataset("ai4bharat/sangraha", "hi", split="train[:2000]")
mixed = concatenate_datasets([english_data, hindi_data]).shuffle(seed=42)
```

**Strategy 2 — Language detection + translation pipeline:**
```python
from langdetect import detect
from transformers import pipeline

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")

def process_query(query):
    lang = detect(query)
    if lang == "hi":
        english_query = translator(query)[0]["translation_text"]
        return sarathi_answer(english_query)
    return sarathi_answer(query)
```

---

## Evaluation & Testing

```python
from nltk.translate.bleu_score import sentence_bleu
import numpy as np

def evaluate_bleu(predictions, references):
    scores = []
    for pred, ref in zip(predictions, references):
        score = sentence_bleu([ref.split()], pred.split())
        scores.append(score)
    return np.mean(scores)
```

### Evaluation Targets

| Metric | Target | Method |
|---|---|---|
| BLEU Score | > 0.30 | Automated |
| F1 (Law QA) | > 0.75 | Automated |
| Human Eval | > 4/5 | Manual rating |
| Latency | < 5s | Benchmark |

---

## Deploying to Hugging Face

```bash
huggingface-cli login
```

```python
model.push_to_hub("david0154/Sarathi-AI")
tokenizer.push_to_hub("david0154/Sarathi-AI")

from huggingface_hub import upload_folder
upload_folder(
    folder_path="./faiss_index",
    repo_id="david0154/Sarathi-AI-VectorDB",
    repo_type="dataset"
)
```

---

## Roadmap

- [x] Architecture design
- [x] Indian data pipeline (Law + Religion + Travel)
- [x] FAISS vector store
- [x] RAG query pipeline
- [ ] QLoRA fine-tuning (in progress)
- [ ] Bengali language fine-tuning
- [ ] Gradio / FastAPI web demo
- [ ] Google Maps API integration (travel)
- [ ] Vision-ready multimodal pipeline
- [ ] Android integration (David AI SDK)
- [ ] Mobile-optimized GGUF model export

---

## License

MIT License — © 2025 David, Nexuzy Lab, Kolkata, India

---

<p align="center">Made with ❤️ in Kolkata, India by <strong>David @ Nexuzy Lab</strong></p>
