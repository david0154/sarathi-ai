# training/qlora_config.py — LoRA / QLoRA hyperparameter config
from peft import LoraConfig
from transformers import BitsAndBytesConfig
import torch


def get_bnb_config() -> BitsAndBytesConfig:
    """4-bit quantization config optimized for T4 Colab."""
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )


def get_lora_config() -> LoraConfig:
    """LoRA adapter config for Mistral 7B."""
    return LoraConfig(
        r=8,                             # Rank — higher = more expressive but larger
        lora_alpha=16,                   # Alpha = 2*r (standard)
        target_modules=[
            "q_proj",                   # Query projection
            "v_proj",                   # Value projection
            "k_proj",                   # Key projection
            "o_proj",                   # Output projection
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )


# Training hyperparameters (Colab T4 optimized)
TRAINING_CONFIG = {
    "output_dir": "./sarathi-qlora-output",
    "num_train_epochs": 3,
    "per_device_train_batch_size": 2,
    "gradient_accumulation_steps": 4,   # Effective batch = 8
    "learning_rate": 2e-4,
    "fp16": True,
    "logging_steps": 50,
    "save_steps": 500,
    "warmup_steps": 100,
    "lr_scheduler_type": "cosine",
    "optim": "paged_adamw_8bit",        # Memory-efficient optimizer
    "report_to": "none",
    "dataloader_num_workers": 0,
    "remove_unused_columns": False,
}
