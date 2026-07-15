# Phase 2: Retrieval-Augmented Generation (RAG)

## Objective

Build a RAG pipeline over a corpus of Anthropic docs — chunking, embedding, vector storage, retrieval, and generation — then evaluate it automatically using RAGAS.

## What's here

| Path | Purpose |
|---|---|
| `corpus/` | 7 Anthropic docs pages fetched and cleaned as `.txt` files |
| `corpus/fetch_docs.py` | Script to re-fetch and clean the corpus |
| `ingestion/chunker.py` | Recursive character text splitter with overlap |
| `ingestion/embedder.py` | `all-MiniLM-L6-v2` wrapper (384-dim, CPU-only) |
| `ingestion/indexer.py` | Qdrant upsert client |
| `ingestion/pipeline.py` | Orchestrator: chunk → embed → index all corpus files |
| `api/retriever.py` | Embeds a query and searches Qdrant for top-k chunks |
| `api/generator.py` | Formats context + question, calls `claude-sonnet-4-6` |
| `api/main.py` | FastAPI app with `/ask` and `/health` endpoints |
| `prompts/rag_answer/v1.yaml` | Versioned RAG answer prompt |
| `eval/golden_qa.json` | 7 hand-labelled QA pairs (one per corpus doc) |
| `eval/run_eval.py` | RAGAS harness — faithfulness, relevancy, precision, recall |
| `eval/reports/` | Timestamped JSON eval reports |
| `docker/Dockerfile` | API service image (build context: repo root) |
| `docker/docker-compose.yml` | Qdrant + API stack |
| `tests/` | Unit tests for chunker, embedder, and retriever |

## Setup

```bash
cd phase-2-rag
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp ../.env.example .env
# add your ANTHROPIC_API_KEY to .env
```

## Run the ingestion pipeline

Qdrant must be running before indexing:

```bash
docker run -d -p 6333:6333 qdrant/qdrant
PYTHONPATH=. python ingestion/pipeline.py
```

## Run the API

```bash
PYTHONPATH=. uvicorn api.main:app --reload
```

Test it:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is prompt caching?"}'
```

## Run with Docker Compose

Starts Qdrant + API together (note: run the ingestion pipeline separately first to populate Qdrant):

```bash
cd docker
docker compose up --build
```

## Run the eval harness

```bash
PYTHONPATH=.. python eval/run_eval.py
```

Scores are printed to stdout and saved to `eval/reports/<timestamp>.json`.

## Run tests

```bash
source .venv/bin/activate
PYTHONPATH=. pytest
```

All tests run without Docker or an API key (Qdrant is mocked in retriever tests).

## Eval results (baseline)

| Metric | Score |
|---|---|
| Faithfulness | 0.88 |
| Answer Relevancy | 0.75 |
| Context Precision | 0.57 |
| Context Recall | 0.57 |

Faithfulness is high — Claude sticks to retrieved context. Precision and recall at 0.57 indicate retrieval is the bottleneck; chunk size and `top_k` tuning are the levers to pull.

## Definition of Done (from ROADMAP.md)

> You have a Dockerized RAG service with an automated eval report (JSON/HTML) generated on each pipeline run.

- [x] Ingestion pipeline: chunking + embedding + Qdrant storage
- [x] FastAPI `/ask` endpoint wiring retrieval and generation
- [x] Prompts loaded from versioned YAML via `shared/prompt_manager`
- [x] RAGAS eval harness with faithfulness, answer relevancy, context precision, context recall
- [x] Hand-labelled golden QA set (7 questions, one per corpus doc)
- [x] Eval report saved as timestamped JSON on each run
- [x] Dockerized with `docker-compose.yml` (Qdrant + API)
- [x] Tests pass without Docker or API key
- [x] `docs/journal/week-03.md` filled in
