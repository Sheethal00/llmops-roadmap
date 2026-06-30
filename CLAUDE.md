# CLAUDE.md

This file gives Claude Code the context and instructions needed to scaffold, build, and incrementally extend this LLM Ops learning roadmap repository.

## Project Overview

This repo is a hands-on, phase-by-phase learning path for becoming an LLM Ops engineer (see `ROADMAP.md`), culminating in a capstone project (see `PROJECT.md`). Each phase is a self-contained, runnable mini-project. Claude Code's job is to scaffold each phase directory, implement the assignment described in `ROADMAP.md` for that phase, write tests, and keep the repo in a runnable state at every step.

Read `ROADMAP.md`, `PROJECT.md`, and `REPO_STRUCTURE.md` in full before doing any work. They are the source of truth for scope, ordering, and Definition of Done per phase.

## Hardware & Environment Constraints

This machine is a **4-core Intel i7-6500U, CPU-only (no GPU), 14 GB RAM**. All tool and model choices must respect these limits:

- **Primary LLM (all phases except Phase 4):** Anthropic API, model `claude-sonnet-4-6`. Never attempt to run a local model for primary LLM tasks — always use the hosted API.
- **Phase 4 local inference:** Use **Ollama** with 3B-class quantized models (e.g., `llama3.2:3b-instruct-q4_K_M` or `qwen2.5:3b-q4_K_M`). Do not use vLLM or TGI — both require a CUDA GPU and will OOM or crash on this machine.
- **Phase 3 fine-tuning:** Data preparation, tokenization, and dataset formatting run locally. Actual LoRA/QLoRA training must happen on **Google Colab's free GPU tier** (T4). Deliver a Colab notebook as the primary training artifact alongside the local data-prep scripts.
- **Single heavy-service rule:** Never run more than one heavy local service at a time. "Heavy" means: Ollama with a loaded model, any Docker Compose stack that includes a vector DB or embedding service, or a local batch embedding job. Shut the previous service down before starting a new one — the machine will swap and freeze otherwise.

## How to Work in This Repo

1. **Always work one phase at a time.** Do not scaffold later phases before earlier ones are functional. If asked to "build phase 4," first verify phases 0-3 exist and at least have working READMEs/stubs; flag gaps instead of silently skipping them.
2. **Mirror `REPO_STRUCTURE.md` exactly.** Do not invent alternate directory layouts. If a needed file/folder isn't listed there, add it to `REPO_STRUCTURE.md` first, then create it.
3. **Every phase directory must be independently runnable.** Include its own `README.md` (objective, setup, run instructions, Definition of Done copied from `ROADMAP.md`) and its own dependency file (`requirements.txt` or `pyproject.toml`). Don't assume a single global virtualenv across phases — some (e.g., phase-4 Ollama, phase-3 PEFT data-prep) have heavy or conflicting dependencies. Respect the single-heavy-service rule in the Hardware section above.
4. **Prompts are never hardcoded.** Any LLM call must load its prompt from a versioned file under the relevant `prompts/` directory via `shared/prompt_manager`. If `shared/prompt_manager` doesn't exist yet, build it first (it's the Phase 1 deliverable) before any phase that calls an LLM.
5. **Default to local/free-tier-friendly choices** unless the user has configured otherwise: Qdrant or pgvector (self-hostable) as the default vector DB, GitHub Actions for CI/CD, Anthropic's API (model `claude-sonnet-4-6`) for any "primary LLM" calls, and Ollama with a 3B quantized model for Phase 4 local inference. See the Hardware & Environment Constraints section above for machine-specific model and service defaults — those override any generic guidance in this rule. Never assume a specific cloud provider unless told — ask or default to a documented choice in the phase README.
6. **Write tests for every assignment**, not just the happy path: at minimum, one test that exercises the core function/pipeline, one that checks a failure mode (e.g., empty retrieval, malformed prompt response), and — from Phase 5 onward — an eval-style test using the golden sets described in the roadmap.
7. **Keep `docs/journal/week-NN.md` updated** with a short summary of what was built and key decisions/tradeoffs whenever a phase is completed or substantially advanced. This is the running learning log — write it as if explaining decisions to a future engineer onboarding to the repo, not as a diary.
8. **Never commit secrets.** All API keys/config go through `.env` (gitignored) with `.env.example` kept up to date with required variable names (no real values).
9. **CI must stay green.** After implementing or changing anything in a phase, run that phase's tests and the root `ci.yml` lint/test locally before considering the task done. If you add a new phase's CI workflow, follow the `eval-gate.yml` template pattern referenced in `REPO_STRUCTURE.md` rather than writing one-off pipelines.
10. **Capstone reuses shared modules.** When building `capstone/`, prefer importing from `shared/` (prompt_manager, llm_clients, eval_lib) over re-implementing logic already built in earlier phases. If something in `shared/` needs to change to support the capstone, update it and re-run tests for every phase that depends on it.

## Definition of Done for Any Task in This Repo

A phase or task is NOT done until:
- The code runs end-to-end via the instructions in its own `README.md`
- Tests pass (`pytest` or equivalent for that phase)
- The phase's "Definition of Done" bullet from `ROADMAP.md` is explicitly satisfied — state how, in the phase README
- No secrets are committed; `.env.example` is current
- `docs/journal/` has an entry summarizing what changed

## Useful Commands (establish/maintain these as the repo grows)

```bash
# Run a specific phase's tests
cd phase-N-<name> && pytest

# Run root-level lint/test across all phases
make ci          # or: bash scripts/ci.sh — create this if it doesn't exist

# Start a phase's local service (e.g., RAG API)
cd phase-2-rag && docker compose up
```

If `make`/`scripts/ci.sh` don't exist yet, create them as part of the first scaffolding pass — they're the canonical entry points for both Claude Code and human contributors going forward.

## What to Ask the User Before Proceeding

If any of the following are ambiguous when starting a phase, ask rather than guessing:
- Which cloud provider (if any) to target for Phase 7 Terraform modules
- Which vector DB to standardize on if the user has a preference different from the default (Qdrant)
- Whether the capstone's "support copilot" should use a real or synthetic knowledge base

Note: Phase 3/4 model-size and runtime choices are already resolved by the Hardware & Environment Constraints section — do not ask about them.

## Out of Scope for Claude Code in This Repo

- Do not provision real cloud infrastructure or apply Terraform against live accounts without explicit user confirmation of the target account/project.
- Do not fine-tune models beyond small open-weight models (≤ ~3B params) unless the user confirms they have the compute budget for larger runs.
- Do not add tracking/analytics or telemetry beyond what's explicitly part of the Phase 6 observability assignment.
