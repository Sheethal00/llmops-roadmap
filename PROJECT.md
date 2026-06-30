# Capstone Project: End-to-End "Support Copilot" LLM Ops System

## Goal
Build and operate a production-grade LLM application — a customer support copilot that answers questions from a knowledge base, escalates to tools/agents when needed, and is fully observable, evaluated, secured, and deployable via CI/CD — demonstrating every skill from the roadmap.

## Functional Scope
1. **Ingestion pipeline**: pulls docs (e.g., a public product's help center, or your own docs/markdown corpus), chunks, embeds, and indexes into a vector DB on a schedule.
2. **RAG API**: FastAPI service that answers user questions using retrieval + generation, with citations to source docs.
3. **Agentic escalation**: when the RAG confidence is low or the user asks for an action (e.g., "check my order status"), an agent uses tools (mocked order-lookup API, ticket-creation tool) via function calling/MCP to complete the task.
4. **Guardrails**: PII redaction on inputs/outputs, prompt-injection detection, content moderation on outputs.
5. **Evaluation harness**: golden-set regression tests (RAG accuracy, agent task success) gated in CI.
6. **Observability**: full tracing (Langfuse/OpenTelemetry) of every request — retrieval, generation, tool calls, cost, latency — plus a cost/latency dashboard.
7. **Deployment**: containerized, deployed via Terraform-provisioned infra, GitHub Actions CI/CD with staged rollout (staging → prod) and automated rollback.
8. **Incident readiness**: alerting on cost spikes and guardrail trip-rate, with a documented runbook.

## Non-Functional Requirements
- p95 latency target documented and load-tested
- Cost-per-request tracked and visible on a dashboard
- All prompts and RAG index configs versioned (no hardcoded prompt strings)
- Rollback to previous prompt/model/index version achievable in under 5 minutes

## Deliverables Checklist
- [ ] Ingestion pipeline (scheduled job, idempotent re-indexing)
- [ ] RAG API with citations
- [ ] Agent with at least 2 tools and bounded iteration/cost
- [ ] Guardrail layer (PII + injection + moderation) with test cases
- [ ] Eval suite (30+ RAG cases, 10+ agent trajectory cases) wired into CI
- [ ] Observability dashboard (traces + cost/latency)
- [ ] Terraform modules for all infra
- [ ] CI/CD pipeline: eval gate → build → staging deploy → manual prod promotion → rollback job
- [ ] Incident runbook + at least one live alert
- [ ] README with architecture diagram and a 5-minute demo walkthrough (recorded or written)

## Suggested Timeline (4 weeks)
- Week 1: Ingestion + RAG API + baseline evals
- Week 2: Agent + tools + guardrails
- Week 3: Observability + CI/CD + IaC
- Week 4: Load testing, incident runbook, polish, demo

## Evaluation Rubric (self-assess against this before calling it done)
| Area | Criteria |
|---|---|
| Correctness | RAG eval accuracy ≥ 85% on golden set; agent task success ≥ 80% |
| Reliability | All agent calls bounded by retries/timeouts; no infinite loops in load test |
| Observability | Every request traceable end-to-end with cost attached |
| Security | Injection test suite passes; PII redaction verified on sample data |
| Operability | One-command deploy; rollback tested and timed |
| Documentation | A new engineer could onboard using only the README + docs/ folder |
