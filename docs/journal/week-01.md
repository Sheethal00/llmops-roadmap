# Week 01 — Phase 0: Foundations Refresh

**Status:** Complete

## What was built

- Scaffolded root repo structure: `README.md`, `.gitignore`, `.env.example`, `docs/`, `phase-0-foundations/`.
- Wrote a full MLOps vs LLMOps comparison in `phase-0-foundations/notes.md` across 5 lifecycle stages using a support-ticket classifier as the running example.
- Added visual HTML comparison at `docs/architecture/mlops-llmops.html`.

## Key insights

- **Labeled data relocates, not disappears.** In MLOps it's training fuel. In LLMOps it comes back as an eval set — but you can ship on day one with zero labels.
- **The prompt is a data artifact.** It encodes the label schema, rules, and examples. It needs to be versioned, reviewed, and deployed like code — which is exactly what Phase 1 (PromptManager) solves.
- **Adding a new category exposes the biggest difference.** MLOps: re-label data + retrain (days). LLMOps: edit one line in the prompt + re-run eval (minutes).
- **Evaluation gets harder, not easier.** A single F1 score becomes a checklist: label accuracy + format compliance + faithfulness + LLM-as-judge. The model can be confidently wrong with no error thrown.
- **Drift can come from the vendor.** You don't own the model — Anthropic can update it silently. A golden set run daily is your only early warning system.

## Decisions and tradeoffs

- Used a support-ticket classifier as the comparison vehicle because it is simple enough to understand quickly but rich enough to show differences at every stage (data labeling, schema changes, eval, deployment artifacts).
- Chose to document both prompt-only and fine-tuning options under LLMOps data/training to show the full spectrum rather than treating LLMOps as purely zero-shot.

## Open questions going into Phase 1

- How should prompt versions be stored — flat files, YAML with metadata, a database?
- How do you diff two prompt versions' *outputs* (not just text) on the same input set?
- What metadata belongs on a prompt artifact (version, author, model, temperature, date)?
