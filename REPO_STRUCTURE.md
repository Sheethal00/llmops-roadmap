# Repository Structure

This is the structure for the roadmap learning repo. Each phase gets its own working directory so assignments are isolated, reproducible, and individually CI-testable. The capstone lives under `capstone/` and reuses modules from earlier phases where sensible.

```
llmops-roadmap/
├── README.md                       # overview, how to navigate the repo, progress tracker
├── ROADMAP.md                      # the full roadmap (phases, topics, resources, assignments)
├── PROJECT.md                      # capstone project specification
├── CLAUDE.md                       # instructions for Claude Code to scaffold/build this repo
├── .gitignore
├── .env.example
├── docs/
│   ├── journal/                    # weekly learning logs, one .md per week
│   │   └── week-01.md
│   ├── architecture/               # diagrams (mermaid/png) per phase and for capstone
│   └── glossary.md                 # LLMOps terms as you learn them
│
├── phase-0-foundations/
│   └── notes.md                    # comparison write-up (MLOps vs LLMOps)
│
├── phase-1-prompt-mgmt/
│   ├── prompts/                    # versioned prompt YAML/JSON files
│   ├── prompt_manager/             # CLI tool source
│   ├── tests/
│   └── README.md
│
├── phase-2-rag/
│   ├── ingestion/                  # chunking + embedding + indexing pipeline
│   ├── api/                        # FastAPI RAG service
│   ├── eval/                       # RAGAS eval harness + golden QA set
│   ├── docker/
│   └── README.md
│
├── phase-3-finetuning/
│   ├── data/                       # curated fine-tuning dataset (or scripts to build it)
│   ├── train/                      # LoRA/QLoRA training scripts
│   ├── model_card.md
│   └── README.md
│
├── phase-4-serving/
│   ├── vllm/                       # Dockerfile + config for vLLM deployment
│   ├── benchmarks/                 # load test scripts (locust/k6) + reports
│   └── README.md
│
├── phase-5-evaluation/
│   ├── golden_sets/                # eval datasets per system under test
│   ├── eval_runner/                # promptfoo/DeepEval config + CI integration
│   └── README.md
│
├── phase-6-observability/
│   ├── tracing/                    # Langfuse/OpenTelemetry instrumentation
│   ├── guardrails/                 # PII redaction, injection detection configs
│   └── README.md
│
├── phase-7-deployment/
│   ├── terraform/                  # IaC modules (vector db, inference endpoint, secrets)
│   ├── .github/workflows/          # CI/CD pipeline defs for this phase's services
│   └── README.md
│
├── phase-8-agents/
│   ├── agent/                      # LangGraph/MCP-based agent implementation
│   ├── tools/                      # tool definitions (mocked APIs)
│   ├── eval/                       # trajectory evals
│   └── README.md
│
├── phase-9-security/
│   ├── runbooks/                   # incident response playbooks
│   ├── alerts/                     # alert rule configs
│   └── README.md
│
├── capstone/
│   ├── ingestion/
│   ├── api/
│   ├── agent/
│   ├── guardrails/
│   ├── eval/
│   ├── observability/
│   ├── terraform/
│   ├── .github/workflows/
│   ├── docs/
│   │   ├── architecture.md
│   │   └── demo-walkthrough.md
│   └── README.md
│
├── shared/
│   ├── prompt_manager/             # promoted, reusable version of phase-1 tool
│   ├── llm_clients/                # thin wrappers around model provider SDKs
│   └── eval_lib/                   # shared eval utilities reused across phases/capstone
│
└── .github/
    └── workflows/
        ├── ci.yml                  # root-level lint/test across all phase dirs
        └── eval-gate.yml           # template reused/imported by phase and capstone workflows
```

## Conventions
- Every phase folder has its own `README.md` stating: objective, how to run it, and Definition of Done (copied from ROADMAP.md).
- Every phase folder has its own `requirements.txt` or `pyproject.toml` — keep dependencies isolated per phase to avoid version conflicts between, e.g., vLLM and PEFT.
- Prompts are never hardcoded in Python files — always loaded from `prompts/` via the shared `prompt_manager`.
- All eval runs write a timestamped report to `eval/reports/` (gitignored except for the latest baseline used in CI).
- Secrets only ever live in `.env` (gitignored) or in the cloud secrets manager provisioned by Terraform — never committed.
