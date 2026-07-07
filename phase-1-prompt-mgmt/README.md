# Phase 1: Prompt Engineering & Prompt Lifecycle Management

## Objective

Build a reusable PromptManager that treats prompts as versioned, reviewable
artifacts — not strings buried in code. By the end you can roll back a prompt
the same way you roll back a config change.

## What's here

| Path | Purpose |
|---|---|
| `prompts/ticket_classifier/` | Two versioned prompt files (v1 zero-shot, v2 few-shot) |
| `prompt_manager/` | Click CLI (`list`, `show`, `run`, `diff`, `history`) |
| `tests/` | Unit tests for loader, renderer, and diff (no API key needed) |
| `../../shared/prompt_manager/` | Reusable library imported by this CLI and all later phases |

## Setup

```bash
cd phase-1-prompt-mgmt
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp ../.env.example .env
# add your ANTHROPIC_API_KEY to .env
```

## CLI Commands

```bash
# List all prompts and their versions
python -m prompt_manager list

# Inspect a prompt's metadata and template
python -m prompt_manager show ticket_classifier
python -m prompt_manager show ticket_classifier --version 1

# Render and call the LLM
python -m prompt_manager run ticket_classifier \
  --vars '{"ticket": "My card was charged twice"}'

# Compare two versions side by side
python -m prompt_manager diff ticket_classifier --v1 1 --v2 2 \
  --vars '{"ticket": "My card was charged twice"}'

# Show full version history
python -m prompt_manager history ticket_classifier
```

## Running Tests

All tests mock the LLM — no API key needed.

```bash
pytest
```

## Prompt File Format

Prompts live at `prompts/<name>/v<N>.yaml`:

```yaml
name: my_prompt
version: 1
description: What this prompt does
author: your name
model: claude-sonnet-4-6
params:
  temperature: 0.0
  max_tokens: 512
system: |
  You are a {{ role }}.
template: |
  Input: {{ variable_name }}
  ...
```

Variables in `system` and `template` are Jinja2 expressions.
Pass them at runtime with `--vars '{"variable_name": "value"}'`.

## Adding a New Prompt Version

1. Copy the latest YAML to the next version number: `cp prompts/my_prompt/v1.yaml prompts/my_prompt/v2.yaml`
2. Edit the new file — update `version: 2` and change the template.
3. Use `diff` to compare outputs before promoting: `python -m prompt_manager diff my_prompt --v1 1 --v2 2 --vars '{...}'`
4. Roll back anytime by pinning `--version 1` in your app.

## Definition of Done (from ROADMAP.md)

> You have a reusable "PromptManager" module with version history and can roll back a prompt like you would a config change.

- [x] Prompts stored as versioned YAML with metadata (version, author, model, params)
- [x] Jinja2 templating with strict variable checking
- [x] `run` command calls Anthropic API via `shared/prompt_manager`
- [x] `diff` command compares two versions' outputs on the same input
- [x] `history` command lists all versions with metadata
- [x] All tests pass without an API key
- [x] No prompt strings hardcoded — all loaded from `prompts/` via `PromptLoader`
- [ ] `docs/journal/week-02.md` filled in
