# src/pipeline.py — Sarathi AI RAG Pipeline (end-to-end)
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from .vectorstore import load_vectorstore, search
from .config import MODEL_NAME, MAX_NEW_TOKENS, TEMPERATURE, TOP_K_RETRIEVAL, SYSTEM_PROMPT
import torch


class SarathiAI:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.db = None

    def load_model(self):
        """Load Mistral 7B in 4-bit quantization."""
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            quantization_config=bnb_config,
            device_map="auto"
        )
        print("✅ Sarathi AI model loaded!")

    def load_vectorstore(self):
        """Load FAISS vector store."""
        self.db = load_vectorstore()
        print("✅ Vector store loaded!")

    def query(self, user_input: str) -> str:
        """Run RAG pipeline for a user query."""
        if self.db is None:
            return "Error: Vector store not loaded."
        if self.model is None:
            return "Error: Model not loaded."

        # Retrieve relevant context
        results = search(self.db, user_input, k=TOP_K_RETRIEVAL)
        context = "\n\n".join([r.page_content for r in results])

        # Build prompt
        prompt = f"""{SYSTEM_PROMPT}

Context from knowledge base:
{context}

User: {user_input}
Sarathi:"""

        # Generate response
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=TEMPERATURE,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("Sarathi:")[-1].strip()


# Singleton instance
sarathi = SarathiAI()
