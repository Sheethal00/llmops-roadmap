# Week 02 — Phase 1: Prompt Engineering & Prompt Lifecycle Management

**Status:** Complete

## What was built

- `shared/prompt_manager/` — reusable library: `PromptLoader`, `render_prompt`, `LLMClient`, `compare_versions`.
- `phase-1-prompt-mgmt/prompt_manager/` — Click CLI with five commands: `list`, `show`, `run`, `diff`, `history`.
- `phase-1-prompt-mgmt/prompts/ticket_classifier/` — two versioned prompt files: v1 (zero-shot), v2 (few-shot with 3 examples covering all categories).
- `phase-1-prompt-mgmt/tests/` — 12 unit tests covering loader, renderer, and diff; all pass without a real API key.

## Key decisions

- **Prompts stored as YAML files** under `prompts/<name>/v<N>.yaml`. Version number is part of the filename so discovery is a simple glob — no database or index needed.
- **`PromptSpec` is a plain dataclass**, not a Pydantic model. Enough for this phase; if validation becomes important in later phases, it can be upgraded.
- **`LLMClient` takes `system` and `user` as separate strings** (not a combined prompt), matching the Anthropic Messages API structure directly. This avoids any re-parsing downstream.
- **`compare_versions` takes `loader` and `client` as arguments** (dependency injection) so tests can pass a mock client without hitting the API. Kept tests fast and free.
- **`StrictUndefined` in Jinja2** — missing template variables raise immediately instead of silently rendering blank. Fail-fast is safer for prompt engineering where a blank variable produces subtly wrong output.

## Tradeoffs

- **Version numbers are integers in filenames** (`v1.yaml`, `v2.yaml`) — simple to discover and sort, but doesn't support branching or named variants (e.g., `v2-cot.yaml`). Fine for this learning context.
- **No rollback command in the CLI** — rolling back means just loading an older version by number, which `run --version N` already handles. A dedicated `rollback` command could write a symlink or alias, but felt like over-engineering for now.
- **`try/except ImportError` for relative imports** in modules with `__main__` blocks — needed because relative imports break when a file is run directly as a script. A cleaner alternative would be a separate `__main__.py` entry point for every module, but the try/except is simpler.

## Open questions going into Phase 2

- Which corpus to build the RAG pipeline over — needs a decision before scaffolding the ingestion pipeline.
- Whether to use Qdrant or pgvector as the vector DB — Qdrant is simpler to spin up in Docker for local dev.
- How to structure the held-out QA evaluation set — synthetic (LLM-generated) vs. hand-labelled golden questions.
