# Phase 3: Fine-tuning, Adapters & Model Customization

## Objective

Fine-tune a small open-weight model (e.g., Llama 3.2 1B/3B or Qwen2.5 1.5B) using LoRA on a narrow task (e.g., a custom classification or style-transfer dataset). Data preparation runs locally; actual LoRA/QLoRA training happens on Google Colab's free GPU tier (T4).

## Topics

- When to fine-tune vs prompt vs RAG (decision framework)
- Parameter-efficient fine-tuning: LoRA/QLoRA, instruction tuning, RLHF/DPO at a conceptual level
- Dataset curation for fine-tuning (format, quality filtering, dedup, contamination checks)
- Model registries for fine-tuned LLM artifacts (Hugging Face Hub, MLflow)

## Resources

- Hugging Face PEFT library docs
- "LoRA: Low-Rank Adaptation" paper (skim)
- Hugging Face course: "Fine-tuning a pretrained model"
- Weights & Biases LLM fine-tuning tutorials

## Assignment

Fine-tune a small open-weight model (e.g., Llama 3.2 1B/3B or Qwen2.5 1.5B) using LoRA on a narrow task (e.g., a custom classification or style-transfer dataset). **Hardware split:** run data preparation, formatting, and tokenization locally; run the actual LoRA/QLoRA training on **Google Colab's free GPU tier (T4)** and provide the training Colab notebook as a primary artifact. Track the run with MLflow or W&B (hyperparameters, loss curves, eval metrics) and push the adapter to Hugging Face Hub or a private registry.

## Setup

```bash
cd phase-3-finetuning
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Create .env from example if needed
cp ../.env.example .env
# Add any required API keys (e.g., for dataset generation if using an LLM)
```

## Run Data Preparation

```bash
# Generate synthetic dataset (example command, specific script might vary)
PYTHONPATH=. python data/generate_dataset.py

# Prepare dataset for fine-tuning (tokenize, split)
PYTHONPATH=. python data/prepare_dataset.py
```

## Run Fine-tuning

The actual LoRA training is done on Google Colab. Open `notebooks/train_lora.ipynb` in Colab to run the training.

## Definition of Done (from ROADMAP.md)

> A versioned LoRA adapter in a registry, a Colab training notebook with a full experiment run logged (loss curves, eval metrics), and a one-page model card describing intended use, training data, and known limitations.

- [x] Data preparation, formatting, and tokenization scripts (`data/generate_dataset.py`, `data/prepare_dataset.py`)
- [x] Google Colab notebook for LoRA/QLoRA training (`notebooks/train_lora.ipynb`)
- [x] Tracking of run with MLflow or W&B (hyperparameters, loss curves, eval metrics)
- [x] Pushing the adapter to Hugging Face Hub or a private registry
- [x] Model card describing intended use, training data, and known limitations (`model_card.md`)
- [x] `docs/journal/week-NN.md` (for the current week) filled in
- [x] Tests pass (for data preparation, if applicable)
