# LLM Ops Engineer Roadmap (for engineers with some MLOps background)

This roadmap assumes you already know: Python, basic ML lifecycle (train/eval/deploy), Docker, REST APIs, Git, and basic CI/CD. It takes you from "MLOps engineer" to "LLM Ops engineer" — someone who can reliably build, deploy, evaluate, secure, and operate LLM-powered systems in production.

Total duration: ~14 weeks (part-time, 8-10 hrs/week). Each phase has: Topics, Resources, Assignment, and a Definition of Done.

> **Machine defaults (4-core i7-6500U, CPU-only, 14 GB RAM):**
> Primary LLM for all phases → Anthropic API (`claude-sonnet-4-6`).
> Phase 4 local inference → Ollama + 3B quantized model (no GPU available; vLLM/TGI are out of scope).
> Phase 3 fine-tuning → data prep locally, LoRA training on Google Colab free GPU tier (T4).
> Resource rule → never run more than one heavy local service (Ollama, vector DB stack, batch embedder) at the same time.

---

## Phase 0: Foundations Refresh (Week 1)

### Topics
- LLM basics: transformer architecture at a conceptual level, tokens, context windows, embeddings
- Difference between MLOps and LLMOps (data flywheel, prompt as artifact, non-determinism, evaluation challenges)
- Landscape overview: model providers (OpenAI, Anthropic, open-weight via Hugging Face), inference engines (vLLM, TGI), orchestration frameworks (LangChain, LlamaIndex), observability tools (LangSmith, Langfuse, Arize)

### Resources
- "Attention Is All You Need" paper (skim) + 3Blue1Brown "Transformers" video series
- Chip Huyen — *"Building LLM Applications for Production"* blog post and her book *AI Engineering* (O'Reilly, 2025)
- Anthropic docs: https://docs.claude.com (prompting guide, models overview)
- Hugging Face NLP Course (free) — chapters 1-3

### Assignment
Write a 1-page comparison: MLOps pipeline vs LLMOps pipeline for the same use case (e.g., a support-ticket classifier as a traditional ML model vs. as an LLM-prompted classifier). Identify what changes at each lifecycle stage (data, training/tuning, eval, deploy, monitor).

### Definition of Done
You can explain to a peer why "model accuracy" monitoring isn't enough for LLM systems and what replaces it.

---

## Phase 1: Prompt Engineering & Prompt Lifecycle Management (Week 2)

### Topics
- Prompt design patterns: zero/few-shot, chain-of-thought, ReAct, structured output (JSON mode/function calling)
- Prompt versioning and management as code (treating prompts like config/artifacts, not strings buried in code)
- System prompts vs user prompts; guardrail prompts

### Resources
- Anthropic's Prompt Engineering guide: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- OpenAI Cookbook (prompting patterns) — github.com/openai/openai-cookbook
- Promptfoo docs (prompt testing) — promptfoo.dev

### Assignment
Build a small CLI tool that stores prompts as versioned YAML/JSON files (with metadata: version, author, model, params), renders them with Jinja2 templating, and calls an LLM API. Add a `diff` command to compare two prompt versions' outputs on the same input set.

### Definition of Done
You have a reusable "PromptManager" module with version history and can roll back a prompt like you would a config change.

---

## Phase 2: Retrieval-Augmented Generation (RAG) Systems (Weeks 3-4)

### Topics
- Embedding models, vector databases (Pinecone, Weaviate, Qdrant, pgvector, Chroma)
- Chunking strategies, hybrid search (BM25 + vector), reranking
- RAG evaluation metrics: faithfulness, context precision/recall, answer relevancy
- Indexing pipelines as data pipelines (incremental updates, freshness, dedup)

### Resources
- LlamaIndex documentation + "Building and Evaluating RAG" short course (DeepLearning.AI, free)
- LangChain docs — RAG section
- RAGAS library docs (ragas.io) for automated RAG evaluation
- Pinecone learning center articles on chunking and hybrid search

### Assignment
Build a RAG pipeline over a corpus of your choice (e.g., your company docs, a public dataset like SEC filings or Wikipedia subset):
1. Ingestion pipeline with chunking + embedding + storage in a vector DB (containerized).
2. Retrieval + generation API endpoint (FastAPI).
3. Evaluation harness using RAGAS producing faithfulness/relevancy scores on a held-out QA set.

### Definition of Done
You have a Dockerized RAG service with an automated eval report (JSON/HTML) generated on each pipeline run.

---

## Phase 3: Fine-tuning, Adapters & Model Customization (Week 5)

### Topics
- When to fine-tune vs prompt vs RAG (decision framework)
- Parameter-efficient fine-tuning: LoRA/QLoRA, instruction tuning, RLHF/DPO at a conceptual level
- Dataset curation for fine-tuning (format, quality filtering, dedup, contamination checks)
- Model registries for fine-tuned LLM artifacts (Hugging Face Hub, MLflow)

### Resources
- Hugging Face PEFT library docs
- "LoRA: Low-Rank Adaptation" paper (skim)
- Hugging Face course: "Fine-tuning a pretrained model"
- Weights & Biases LLM fine-tuning tutorials

### Assignment
Fine-tune a small open-weight model (e.g., Llama 3.2 1B/3B or Qwen2.5 1.5B) using LoRA on a narrow task (e.g., a custom classification or style-transfer dataset). **Hardware split:** run data preparation, formatting, and tokenization locally; run the actual LoRA/QLoRA training on **Google Colab's free GPU tier (T4)** and provide the training Colab notebook as a primary artifact. Track the run with MLflow or W&B (hyperparameters, loss curves, eval metrics) and push the adapter to Hugging Face Hub or a private registry.

### Definition of Done
A versioned LoRA adapter in a registry, a Colab training notebook with a full experiment run logged (loss curves, eval metrics), and a one-page model card describing intended use, training data, and known limitations.

---

## Phase 4: Serving & Inference Infrastructure (Week 6)

### Topics
- Inference servers: vLLM, Text Generation Inference (TGI), Triton Inference Server
- Batching, continuous batching, KV-cache, quantization (GGUF, AWQ, GPTQ) for cost/latency tradeoffs
- Autoscaling LLM workloads (GPU vs CPU, cold starts), API gateways, request queuing
- Multi-model routing (small model for easy queries, large model for hard ones)

### Resources
- vLLM documentation (docs.vllm.ai)
- Hugging Face TGI docs
- "Efficient Inference" chapters in Chip Huyen's AI Engineering book
- NVIDIA Triton Inference Server quickstart

### Assignment
Deploy a 3B-class quantized open-weight model using **Ollama** (e.g., `llama3.2:3b-instruct-q4_K_M` or `qwen2.5:3b-q4_K_M`) with its OpenAI-compatible REST API. **Note:** vLLM and TGI require a CUDA GPU and are not used here — Ollama's CPU-inference path is the target runtime for this machine. Load test it with `locust` or `k6`, measure p50/p95 latency and throughput at different concurrency levels and quantization sizes (e.g., Q4_K_M vs Q5_K_M), and write a short benchmarking report comparing 2 configurations. Shut down all other heavy services (vector DB, Docker stacks) before running the load test to get stable numbers on this hardware.

### Definition of Done
A reproducible benchmark script + report with latency/throughput tradeoffs for the two Ollama configurations and a recommendation calibrated to CPU-only constraints.

---

## Phase 5: Evaluation & Testing for LLM Systems (Week 7)

### Topics
- Eval types: golden-set regression tests, LLM-as-judge, human eval, adversarial/red-team testing
- Building eval datasets, avoiding eval leakage, statistical significance with small samples
- CI integration: gating prompt/model changes on eval scores before merge
- Tools: promptfoo, RAGAS, DeepEval, OpenAI Evals framework

### Resources
- promptfoo docs (CI integration examples)
- DeepEval docs (confident-ai.com)
- Anthropic's guidance on building evals: https://docs.claude.com (search "evaluate")
- "Your AI Product Needs Evals" — Hamel Husain's blog post

### Assignment
Build an eval suite (using promptfoo or DeepEval) for your Phase 2 RAG service with at least 30 golden test cases. Wire it into a GitHub Actions workflow that runs on every PR touching prompts or retrieval config, and fails the build if accuracy drops below a threshold.

### Definition of Done
A green/red CI check that blocks merges on eval regression, with a published eval report artifact per run.

---

## Phase 6: Observability, Cost & Guardrails (Week 8)

### Topics
- LLM observability: tracing (spans for retrieval, prompt, generation), token/cost tracking, latency dashboards
- Tools: Langfuse, LangSmith, Arize Phoenix, OpenTelemetry GenAI semantic conventions
- Guardrails: input/output content filtering, PII redaction, prompt-injection detection, jailbreak resistance
- Cost monitoring and budget alerting per tenant/feature

### Resources
- Langfuse docs (self-hostable, open source) — langfuse.com/docs
- OpenTelemetry GenAI semantic conventions spec
- NeMo Guardrails docs / Guardrails AI (guardrailsai.com)
- OWASP Top 10 for LLM Applications

### Assignment
Instrument your RAG service with Langfuse (or OpenTelemetry) tracing for every request: capture prompt, retrieved chunks, model response, token counts, cost, and latency per span. Add a guardrail layer (e.g., Guardrails AI or NeMo Guardrails) for PII redaction and basic prompt-injection detection, and add 5 adversarial test cases to your eval suite from Phase 5.

### Definition of Done
A live trace dashboard showing cost/latency per request, plus a guardrail layer with passing/failing test cases for injected adversarial prompts.

---

## Phase 7: Deployment, CI/CD & Infra-as-Code for LLM Systems (Weeks 9-10)

### Topics
- Containerizing LLM services, GPU scheduling on Kubernetes (or managed alternatives: SageMaker, Vertex AI, Bedrock)
- IaC with Terraform for vector DBs, inference endpoints, secrets management
- CI/CD pipelines for prompts, RAG indices, and fine-tuned models (separate pipelines per artifact type)
- Blue/green and canary deployment for prompt/model changes; rollback strategy
- Secrets and API key management (Vault, AWS Secrets Manager)

### Resources
- Kubernetes docs + "Kubernetes for ML" guide (kubeflow.org)
- Terraform Associate learning path (free tier on HashiCorp Learn)
- AWS Bedrock / GCP Vertex AI / Azure AI Studio quickstarts (pick one cloud)
- "Continuous Delivery for Machine Learning" (martinfowler.com/articles/cd4ml.html)

### Assignment
Write Terraform modules to provision: a vector DB instance, an inference endpoint (managed or self-hosted), and secrets storage. Build a GitHub Actions pipeline with 3 stages: (1) run eval suite, (2) build & push container, (3) deploy to staging with a manual approval gate to promote to prod. Implement a rollback job that reverts to the previous prompt/model version on failure.

### Definition of Done
One-command (`terraform apply` + pipeline trigger) deploy from staging to prod with an automated rollback path you've tested by intentionally breaking a deploy.

---

## Phase 8: Agentic Systems & Multi-Step Workflows (Weeks 11-12)

### Topics
- Tool use / function calling, agent loops (ReAct, plan-and-execute), multi-agent orchestration
- Frameworks: LangGraph, CrewAI, Anthropic's agent SDK / Claude Agent SDK patterns, MCP (Model Context Protocol)
- Reliability patterns for agents: retries, timeouts, max-iteration caps, human-in-the-loop checkpoints
- Evaluating agent trajectories (not just final answers)

### Resources
- LangGraph docs (multi-agent orchestration)
- Model Context Protocol spec: modelcontextprotocol.io
- Anthropic's "Building Effective Agents" blog post
- DeepLearning.AI short course: "AI Agents in LangGraph"

### Assignment
Build a tool-using agent (e.g., a research/report-writing agent that searches, retrieves, summarizes, and writes a structured report) using function calling + MCP tools. Add trajectory logging and an eval that scores whether the agent used tools correctly and stayed within iteration/cost budgets.

### Definition of Done
A working agent with bounded retries/cost, full trajectory tracing, and an eval report on 10+ task scenarios including at least 2 designed to test failure handling.

---

## Phase 9: Security, Compliance & Responsible AI Ops (Week 13)

### Topics
- Prompt injection and jailbreak defenses in depth, data exfiltration risks via tool use
- PII/PHI handling, data residency, audit logging for compliance (SOC2/GDPR-aware design)
- Model/data lineage and provenance tracking for audits
- Incident response playbook for LLM-specific failures (hallucination incident, prompt leak, cost spike)

### Resources
- OWASP Top 10 for LLM Applications (detailed read this time)
- NIST AI Risk Management Framework (AI RMF 1.0)
- Anthropic's Responsible Scaling Policy (overview, for context on industry practice)
- "Building Secure GenAI Applications" — Google Cloud whitepaper

### Assignment
Write an incident response runbook for 3 scenarios (prompt injection causing data leak, sudden 10x cost spike, model returning harmful content) including detection signals, escalation steps, and rollback procedures. Add automated alerts (cost threshold, guardrail-trip rate) to your Phase 6 observability stack.

### Definition of Done
A runbook doc + at least one working automated alert that fires in a simulated incident (e.g., you spike token usage in a test and the alert triggers).

---

## Phase 10: Capstone Project (Week 14+)

See `PROJECT.md` for the full capstone specification: an end-to-end "Customer Support Copilot" system that integrates everything from Phases 1-9 (RAG, evals, observability, guardrails, agentic tool use, CI/CD, IaC) into one deployable system.

---

## Suggested Weekly Cadence
Each week: ~2 hrs reading/courses, ~5-6 hrs hands-on assignment, ~1 hr writing up learnings/decisions in your repo's `docs/journal/`.

## Core Tool Stack Used Across This Roadmap
Python, FastAPI, Docker, Kubernetes/Terraform, vLLM, LangChain/LlamaIndex, LangGraph, Hugging Face (PEFT/Hub), a vector DB (Qdrant/pgvector), Langfuse, promptfoo/DeepEval/RAGAS, GitHub Actions, MLflow or W&B.
