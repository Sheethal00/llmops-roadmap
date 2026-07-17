import os
import re

from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer

LABEL2ID = {
    "billing": 0,
    "technical": 1,
    "account": 2,
    "shipping": 3,
    "general": 4,
}

MODEL_NAME = "meta-llama/Llama-3.2-1B"
RAW_DATA_PATH = "data/raw/tickets.jsonl"
OUTPUT_PATH = "data/processed/"
MAX_LENGTH = 128
TEST_SIZE = 0.2
SEED = 42


def encode_label(example):
    example["label"] = LABEL2ID[example["label"]]
    return example


def validate_labels(dataset: DatasetDict):
    """Fail fast if the raw data contains a label not in LABEL2ID."""
    seen = set()
    for split in dataset.values():
        seen.update(split["label"])
    unknown = seen - set(LABEL2ID)
    if unknown:
        raise ValueError(f"Found labels not present in LABEL2ID: {unknown}")


def _normalize(text: str) -> str:
    """Normalize text for dedup comparison: lowercase, collapse whitespace,
    strip punctuation-adjacent noise. This is intentionally more aggressive
    than the stored text so near-identical LLM generations (differing only
    in casing/spacing/trailing punctuation) are still caught."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text


def dedup_raw(raw):
    """Exact/near-duplicate removal on the raw (pre-split) dataset.

    Must run BEFORE train_test_split — deduping after the split does nothing
    to prevent the same ticket (or a near-identical LLM-generated variant)
    from landing in both train and validation, which is what actually
    causes leakage.
    """
    seen = set()
    keep_idx = []
    for i, text in enumerate(raw["text"]):
        key = _normalize(text)
        if not key:
            # empty / whitespace-only generation — quality filter, not dedup,
            # but cheap to drop here too
            continue
        if key in seen:
            continue
        seen.add(key)
        keep_idx.append(i)

    n_dropped = len(raw) - len(keep_idx)
    if n_dropped:
        print(f"Dedup: dropped {n_dropped} duplicate/empty rows out of {len(raw)}")
    return raw.select(keep_idx)


def check_no_contamination(dataset: DatasetDict):
    """Assert train and validation share no examples after normalization.
    This is a safety net, not the primary defense — dedup_raw() above is
    what should actually prevent this from happening. If this ever fires,
    something upstream (e.g. dedup running after the split, or a new split
    call) reintroduced leakage."""
    train_keys = {_normalize(t) for t in dataset["train"]["text"]}
    val_keys = {_normalize(t) for t in dataset["validation"]["text"]}
    overlap = train_keys & val_keys
    if overlap:
        raise ValueError(
            f"Contamination detected: {len(overlap)} examples appear in both "
            f"train and validation after normalization. Example: {next(iter(overlap))!r}"
        )
    print("Contamination check passed: no overlap between train and validation.")


def main():
    # Load
    raw = load_dataset("json", data_files=RAW_DATA_PATH)["train"]
    print(f"Loaded {len(raw)} raw records")

    # Dedup BEFORE splitting — this is what actually prevents leakage
    raw = dedup_raw(raw)

    # Split
    split = raw.train_test_split(test_size=TEST_SIZE, seed=SEED)
    dataset = DatasetDict({"train": split["train"], "validation": split["test"]})

    # Validate + encode labels
    validate_labels(dataset)
    dataset = dataset.map(encode_label)

    # Contamination check (belt-and-suspenders, after split/encode)
    check_no_contamination(dataset)

    # Report label distribution per split — cheap sanity check that dedup
    # or the split didn't skew any one class
    for split_name, split_data in dataset.items():
        counts = {}
        for label_id in split_data["label"]:
            counts[label_id] = counts.get(label_id, 0) + 1
        print(f"{split_name} label distribution: {counts}")

    # Tokenizer setup
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LENGTH,
        )

    # NOTE: "text" is deliberately kept (not passed to remove_columns) so that
    # misclassified examples can be traced back to their original ticket text
    # during error analysis, without needing to reload the raw dataset and
    # re-match by index.
    tokenized_dataset = dataset.map(
        tokenize,
        batched=True,
    )

    # Save
    if os.path.exists(OUTPUT_PATH) and os.listdir(OUTPUT_PATH):
        raise FileExistsError(
            f"'{OUTPUT_PATH}' already exists and is not empty. "
            "Remove it or choose a different output path before re-running."
        )
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    tokenized_dataset.save_to_disk(OUTPUT_PATH)

    print(f"\nSaved processed dataset to '{OUTPUT_PATH}'")
    print(tokenized_dataset)


if __name__ == "__main__":
    main()
