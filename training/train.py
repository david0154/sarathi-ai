# training/train.py — Main QLoRA training script for Sarathi AI
import sys
sys.path.append("..")

import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    TrainingArguments, Trainer,
    DataCollatorForLanguageModeling
)
from peft import get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
from src.config import MODEL_NAME, SYSTEM_PROMPT
from training.qlora_config import get_bnb_config, get_lora_config, TRAINING_CONFIG


def format_instruction(example: dict) -> dict:
    """Format daily_dialog to Sarathi instruction format."""
    dialog = example.get("dialog", [])
    text = f"{SYSTEM_PROMPT}\n\n"
    for i, turn in enumerate(dialog[:6]):
        role = "User" if i % 2 == 0 else "Sarathi"
        text += f"{role}: {turn.strip()}\n"
    return {"text": text}


def main():
    print("🚀 Starting Sarathi AI QLoRA Training...")
    print(f"   Model: {MODEL_NAME}")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Load model in 4-bit
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=get_bnb_config(),
        device_map="auto"
    )

    # Prepare for QLoRA
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, get_lora_config())
    model.print_trainable_parameters()

    # Load and format dataset
    print("📚 Loading dataset...")
    dataset = load_dataset("daily_dialog", split="train[:8000]")
    dataset = dataset.map(format_instruction, remove_columns=dataset.column_names)

    # Tokenize
    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=512,
            padding="max_length"
        )

    tokenized = dataset.map(tokenize, batched=True, remove_columns=["text"])
    print(f"✅ Dataset ready: {len(tokenized)} samples")

    # Training
    training_args = TrainingArguments(**TRAINING_CONFIG)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )

    trainer.train()

    # Save
    output_path = "./sarathi-ai-final"
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print(f"✅ Training complete! Saved to {output_path}")


if __name__ == "__main__":
    main()
