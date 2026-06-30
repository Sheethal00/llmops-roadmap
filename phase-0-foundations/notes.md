# MLOps vs LLMOps: Pipeline Comparison

**Use case:** Support-ticket classifier
- **Version A (MLOps):** A fine-tuned BERT/logistic-regression model that classifies tickets into categories (billing, technical, account, etc.) trained on labeled historical tickets.
- **Version B (LLMOps):** The same classifier reimplemented as a prompted LLM call — the model reads the ticket and returns a structured category + confidence explanation, with no task-specific training.

Compare these two pipelines stage by stage. Fill in each section with your own words before moving to Phase 1.

---

## 1. Data

### MLOps
*What data is needed? How is it prepared? What does a "training example" look like?*

- [ ] Fill in

### LLMOps
*What data is needed? What role does labeled data play (if any) here? What is the "prompt" as a data artifact?*

- [ ] Fill in

### Key differences
*What changes about data collection, labeling, versioning, and freshness requirements?*

- [ ] Fill in

---

## 2. Training / Tuning

### MLOps
*What is the training loop? What hyperparameters matter? How long does it take? What does "done training" mean?*

- [ ] Fill in

### LLMOps
*Is there a training step? What replaces it? What is "prompt engineering" as a workflow? When would you actually fine-tune an LLM here?*

- [ ] Fill in

### Key differences
*Which "knobs" move between approaches? What is the equivalent of a training run in the LLMOps world?*

- [ ] Fill in

---

## 3. Evaluation

### MLOps
*What metrics? How is the eval set constructed? How do you know the model is good enough to ship?*

- [ ] Fill in

### LLMOps
*Why doesn't accuracy alone work? What replaces or supplements it? How do you evaluate a free-text explanation alongside a classification label?*

- [ ] Fill in

### Key differences (this is the Definition-of-Done question — answer it here)
*Why is "model accuracy" monitoring not enough for LLM systems, and what replaces it?*

- [ ] Fill in

---

## 4. Deployment

### MLOps
*How is the model packaged and served? What does a model artifact look like (pickle, ONNX, TorchScript)? How do you roll back?*

- [ ] Fill in

### LLMOps
*What is deployed? (Hint: the prompt is an artifact too.) How do you version and deploy a prompt change vs a model change? What does rollback mean when the model lives behind an API?*

- [ ] Fill in

### Key differences
*What new artifact types are introduced? What new deployment risks appear (latency, cost, non-determinism)?*

- [ ] Fill in

---

## 5. Monitoring

### MLOps
*What signals do you watch in production? What triggers a retraining run? What does "model drift" look like?*

- [ ] Fill in

### LLMOps
*What signals replace or supplement accuracy metrics? Think about: output quality, cost, latency, hallucination rate, user feedback, guardrail trips.*

- [ ] Fill in

### Key differences
*What is "LLM drift" and how would you detect it? What is unique about monitoring non-deterministic, free-text outputs?*

- [ ] Fill in

---

## Summary: What Stays the Same, What Changes

| Lifecycle Stage | MLOps | LLMOps | Biggest change |
|---|---|---|---|
| Data | | | |
| Training / tuning | | | |
| Evaluation | | | |
| Deployment | | | |
| Monitoring | | | |

*Fill in the table last — it should flow naturally from the sections above.*

---

## One-Paragraph Takeaway

*After filling everything in: write 3-5 sentences summarizing the mental model shift from MLOps to LLMOps. This is what you'd say to a peer in a hallway conversation.*

- [ ] Fill in
