# LLM Ops Engineer Roadmap

A hands-on, phase-by-phase learning path from MLOps engineer to LLM Ops engineer. Each phase is a self-contained, runnable mini-project. The capstone integrates everything into a deployable "Customer Support Copilot."

See [`ROADMAP.md`](ROADMAP.md) for the full syllabus, [`PROJECT.md`](PROJECT.md) for the capstone spec, and [`REPO_STRUCTURE.md`](REPO_STRUCTURE.md) for the directory layout.

## Progress

| Phase | Topic | Status |
|-------|-------|--------|
| 0 | Foundations Refresh | In progress |
| 1 | Prompt Engineering & Prompt Lifecycle Management | Not started |
| 2 | Retrieval-Augmented Generation (RAG) Systems | Not started |
| 3 | Fine-tuning, Adapters & Model Customization | Not started |
| 4 | Serving & Inference Infrastructure | Not started |
| 5 | Evaluation & Testing for LLM Systems | Not started |
| 6 | Observability, Cost & Guardrails | Not started |
| 7 | Deployment, CI/CD & Infra-as-Code | Not started |
| 8 | Agentic Systems & Multi-Step Workflows | Not started |
| 9 | Security, Compliance & Responsible AI Ops | Not started |
| 10 | Capstone Project | Not started |

## How to Navigate

- Each `phase-N-*/` folder has its own `README.md` with setup and run instructions.
- Learning notes and decision logs live in [`docs/journal/`](docs/journal/).
- Shared utilities (prompt manager, LLM clients, eval lib) live in [`shared/`](shared/) and are built incrementally starting from Phase 1.

## Machine Defaults

4-core i7-6500U, CPU-only, 14 GB RAM. Primary LLM: Anthropic API (`claude-sonnet-4-6`). Phase 4 local inference: Ollama + 3B quantized model. Phase 3 training: Google Colab free GPU tier. See [`CLAUDE.md`](CLAUDE.md) for full hardware constraints.

## Running Tests

```bash
# Single phase
cd phase-N-<name> && pytest

# All phases (once ci.sh exists)
bash scripts/ci.sh
```
