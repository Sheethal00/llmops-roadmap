import json
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.prompt_manager.loader import PromptLoader
from shared.prompt_manager.renderer import render_prompt
from shared.prompt_manager.client import LLMClient

LABELS = ["billing", "technical", "account", "shipping", "general"]
COUNT_PER_LABEL = 120
OUTPUT_PATH = Path(__file__).parent / "raw" / "tickets.jsonl"
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
NAME = "ticket_classifier_gen"
VERSION = 2
CATEGORY_DEFINITIONS = {
    "billing": "These tickets are about payments, invoices, charges, refunds, or subscription costs.",
    "technical": "These tickets are about bugs, errors, broken features, or the product not working as expected.",
    "account": "These tickets are about login, password, profile settings, or account access issues.",
    "shipping": "These tickets are about delivery, tracking, or lost/delayed packages.",
    "general": (
        "These tickets do NOT mention accounts, logins, passwords, billing, payments, refunds, "
        "subscriptions, orders, shipping, tracking, bugs, errors, or specific technical features. "
        "Instead, write about: general product feedback, feature requests, compliments or complaints "
        "about the company overall, partnership or business inquiries, questions about company policy, "
        "or vague requests that don't clearly belong to a specific support category."
    ),
}


def generate_for_label(label: str, count: int, prompt_spec, llm_client, cat_desc: dict | None = None) -> list[dict]:
    if cat_desc:
        variables = {"label": label, "count": count,"category_definition": cat_desc}
    else:
        variables = {"label": label, "count": count}
    system, user = render_prompt(prompt_spec, variables=variables)
    raw_response = llm_client.run(prompt_spec, system, user)
    try:
        tickets = json.loads(raw_response)
    except json.JSONDecodeError:
        print(f"Failed to parse response for label={label}:\n{raw_response}")
        raise
    return [{"text": text, "label": label} for text in tickets]


def main():
    loader = PromptLoader(PROMPTS_DIR)
    prompt_spec = loader.load(NAME,VERSION)
    llm_client = LLMClient()
    records = []

    for label in LABELS:
        print(f"Generating {COUNT_PER_LABEL} tickets for '{label}'...")
        if VERSION == 1:
            batch = generate_for_label(label, COUNT_PER_LABEL,prompt_spec, llm_client)
        else:
            batch = generate_for_label(label, COUNT_PER_LABEL, prompt_spec, llm_client, CATEGORY_DEFINITIONS)
        records.extend(batch)
        print(f"  done — {len(batch)} tickets")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"\nSaved {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()