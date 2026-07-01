# Phase 0: Foundations Refresh

## Objective

Build a mental model of how LLM-powered systems differ from classical ML systems at every stage of the lifecycle, so that the rest of the roadmap has a "why" behind each tool choice.

## Assignment

Write a 1-page comparison of an MLOps pipeline vs an LLMOps pipeline for the same use case: a support-ticket classifier, first built as a traditional supervised ML model, then rebuilt as an LLM-prompted classifier. Identify what changes at each lifecycle stage.

The comparison lives in [`notes.md`](notes.md). A visual side-by-side reference is at [`docs/architecture/mlops-llmops.html`](../docs/architecture/mlops-llmops.html) — open it in a browser.

## How to Run

Phase 0 is conceptual — there is no code to execute. Read the resources listed in `ROADMAP.md`, then fill in `notes.md`.

Optional: spin up a scratch notebook to experiment with the Anthropic API or Hugging Face tokenizers.

```bash
# (optional) create an isolated env for scratch work
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Definition of Done (from ROADMAP.md)

> You can explain to a peer why "model accuracy" monitoring isn't enough for LLM systems and what replaces it.

Checklist:
- [ ] `notes.md` comparison is filled in — all lifecycle stages addressed
- [ ] You can give a verbal answer to the Definition of Done question above
- [ ] At least 5 new terms added to [`docs/glossary.md`](../docs/glossary.md)
- [ ] `docs/journal/week-01.md` has an entry summarizing key insights
