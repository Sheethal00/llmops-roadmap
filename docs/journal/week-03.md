# Week 03 — Phase 2: Retrieval-Augmented Generation (RAG)

**Status:** Complete

## What was built

- `phase-2-rag/corpus/fetch_docs.py` — scraper that fetches 7 Anthropic docs pages from `platform.claude.com/docs/en/*.md` endpoints (raw markdown), strips code blocks, JSX tags, and MDX components, and saves clean `.txt` files (~158KB total corpus).
- `phase-2-rag/ingestion/chunker.py` — recursive character text splitter: tries separators from coarsest (`\n\n`) to finest (hard character split), then post-processes with overlap by prepending the tail of the previous chunk onto the next.
- `phase-2-rag/ingestion/embedder.py` — thin wrapper around `sentence-transformers` `all-MiniLM-L6-v2` (384-dim, CPU-friendly), always normalises embeddings so dot product equals cosine similarity.
- `phase-2-rag/ingestion/indexer.py` — Qdrant client wrapper; creates collection on first run (skips if exists), upserts points with chunk text and metadata as payload.
- `phase-2-rag/ingestion/pipeline.py` — orchestrator: iterates corpus files, chunks each, batches embeddings, indexes with globally unique IDs via an offset counter.
- `phase-2-rag/api/retriever.py` — embeds a query and searches Qdrant for top-k nearest chunks by cosine similarity, returns payload dicts.
- `phase-2-rag/api/generator.py` — loads prompt from `prompts/rag_answer/v1.yaml` via `shared/prompt_manager`, formats retrieved chunks as numbered context, calls `claude-sonnet-4-6`, returns answer text.
- `phase-2-rag/api/main.py` — FastAPI app with `/ask` (POST) and `/health` (GET) endpoints; wires retriever and generator together.
- `phase-2-rag/prompts/rag_answer/v1.yaml` — versioned RAG answer prompt; system instruction to answer only from context, template with `{{ context }}` and `{{ question }}` variables.
- `phase-2-rag/eval/golden_qa.json` — 7 hand-labelled QA pairs covering all 7 corpus documents.
- `phase-2-rag/eval/run_eval.py` — RAGAS harness: retrieves + generates answers for all golden questions, then scores with faithfulness, answer relevancy, context precision, and context recall using `claude-sonnet-4-6` as the judge LLM and `all-MiniLM-L6-v2` for embeddings.

## Eval results (first run)

| Metric | Score |
|---|---|
| Faithfulness | 0.88 |
| Answer Relevancy | 0.75 |
| Context Precision | 0.57 |
| Context Recall | 0.57 |

## Key decisions

- **Corpus: Anthropic docs (platform.claude.com)** — 7 pages covering prompt caching, context windows, extended thinking, vision, tool use, structured outputs, and multimodal. Chosen because the content is dense, technical, and directly relevant to what we're building.
- **Recursive character splitting** over semantic/sentence splitting — simpler to implement and understand, fast on CPU, respects natural document boundaries (paragraph → line → word → char). Overlap is post-processed by prepending the tail of the previous chunk, not by re-splitting.
- **`all-MiniLM-L6-v2` for embeddings** — 384-dim, CPU-friendly, no GPU required. `normalize_embeddings=True` so retrieval uses plain dot product.
- **Qdrant as vector DB** — self-hostable via Docker, clean Python client, cosine distance matches normalised embeddings. Collection creation is guarded by `collection_exists` check so re-running the pipeline doesn't wipe existing data.
- **Global ID offset in pipeline** — chunk IDs restart at 0 per file, so the pipeline accumulates an offset across files to prevent later files overwriting earlier ones in Qdrant.
- **Prompt loaded from versioned YAML** — reuses `shared/prompt_manager` from Phase 1. Generator never hardcodes the prompt; swapping prompt versions is a one-line change.
- **Hand-labelled golden QA set** — 7 questions written after reading the corpus, one per source document. Ground truth answers written in own words (2-4 sentences) so RAGAS context recall has a meaningful reference to compare against.

## Tradeoffs

- **Retrieval is the bottleneck, not generation** — faithfulness (0.88) is high, meaning Claude sticks to what it retrieves. But precision and recall (0.57) show retrieval is surfacing noisy or incomplete chunks. This is the most common finding in real RAG systems.
- **chunk_size=1000, chunk_overlap=150** — chosen as sensible defaults, not tuned. Chunk size affects the precision/recall tradeoff: larger chunks improve recall (more context per chunk) but hurt precision (more noise per chunk). Tuning this is Phase 5 (optimization) work.
- **top_k=5 fixed** — not tuned. Too few and recall suffers; too many and precision drops. Left as a parameter for future experiments.
- **RAGAS dependency conflicts** — RAGAS pulls in `langchain-community` which tries to import `langchain_community.chat_models.vertexai` (a Google Vertex AI module). Fixed by mocking the missing module before RAGAS imports. Also required configuring both LLM and embeddings explicitly to avoid defaulting to OpenAI.
- **No Docker Compose yet** — Qdrant is run standalone via `docker run`. Docker Compose wrapping the full stack (Qdrant + API) is the remaining Definition of Done item.

## Open questions going into Phase 3

- Whether the LoRA adapter training on Colab should target the same domain (Anthropic docs) or a different narrow task — needs a decision before data prep.
- How to version and store the adapter artifact — Hugging Face Hub (public) vs. MLflow local registry.
