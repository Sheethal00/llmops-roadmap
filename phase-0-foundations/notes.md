# MLOps vs LLMOps: Pipeline Comparison

**Use case:** Support-ticket classifier
- **Version A (MLOps):** A fine-tuned BERT/logistic-regression model that classifies tickets into categories (billing, technical, account, etc.) trained on labeled historical tickets.
- **Version B (LLMOps):** The same classifier reimplemented as a prompted LLM call — the model reads the ticket and returns a structured category + confidence explanation, with no task-specific training.

Compare these two pipelines stage by stage. Fill in each section with your own words before moving to Phase 1.

---

## 1. Data

### MLOps
*What data is needed? How is it prepared? What does a "training example" look like?*

- Input: The input will a text based input. It can represnt the meaning of the ticket whether it related to
          Account, Billing or something Techinal. Each text based input will have a integer label.
          (Account-0, Billing-1, Techinal-2)
- Prep: If I go with logistic regression method then we can use something like TF-IDF to create vectors which 
        will be easy for model to classify the document
- Source: It will be an historical data labbeled by annotators
- A training example is a (text, label) pair
- Scale: classical text classifiers typically need hundreds to thousands of labeled examples per category to generalize well. Worth noting because the LLMOps version needs zero.
- Label schema changes: if you add a new category (e.g., "Refunds"), you need to re-label data and retrain. That friction shows up as a key difference later.


### LLMOps
*What data is needed? What role does labeled data play (if any) here? What is the "prompt" as a data artifact?*

- Option 1: Prompt only LLM
  - Pros - This option does not require any training
  - Input - Will be a prompt with the input text as contect
  - Output - Model will return a json with category, confidence score and reason for the prediction
  - The prompt is a data artifact — this is the key LLMOps insight for this section. In MLOps, your data lives in CSV/parquet files versioned in a data store. In LLMOps, the prompt is your "training signal" — it encodes the label schema, examples, and rules. It needs to be versioned, reviewed, and deployed like code
  - Cons - The confidence score is not reliable since model is trained on general data not specific to our dataset
  - Example prompt
    > You are a support ticket classifier.
    >
    >Categories:
    >
    >Billing → payments, refunds, charges, invoices
    >
    > Account → login, profile, password, permissions
    >
    > Technical → bugs, crashes, errors, app failures
    >
    > Input:
    >
    >"My card was charged twice"
    >
    >Return JSON:
    >{
    >
    > "category": "...",
    >
    > "confidence": float between 0 and 1,
    >
    > "reason": "short explanation"
    >
    >}
- Option 2: Fine-tune an LLM (best if categories become complex)
  - Input - Input text of the ticket
  - Output- Category with confidence score

### Key differences
*What changes about data collection, labeling, versioning, and freshness requirements?*

- In MLOps you need to collect and label data before you can do
  anything. In LLMOps you can ship a working classifier on day one with zero labeled data. Labeled data in LLMOps only becomes relevant later, for building an eval set to measure
  quality — not for training.
- Key difference for labelling MLOps data is if new category is introduced then we may need to update the label. But in LLMOps the prompt take cares of it
- Versioning has to be done for prompt as well

---

## 2. Training / Tuning

### MLOps
*What is the training loop? What hyperparameters matter? How long does it take? What does "done training" mean?*

- Prepare the training data, generate embeddings for ticket text and encode the labels. Split dataset. Train classifier. 
- Key hyperparameters are regularization, no of training iterations etc
- A logistic regression on thousands of tickets trains in seconds to minutes. A fine-tuned BERT takes
  hours on a GPU.
- Model will generate the probabilities for the given embeddings and it is compared with gt lables by computing loss. The key thing here is to minimize the loss (distance between prediction and gt)
- We stop training when validation loss stops improving (early stopping), or when it hit your target metric (e.g., F1 > 0.90) on the held-out eval set

### LLMOps
*Is there a training step? What replaces it? What is "prompt engineering" as a workflow? When would you actually fine-tune an LLM here?*

- Prompt-only approach: No training step at all. The "loop" means, write a prompt → test it on sample tickets → look at outputs → rewrite the prompt → repeat. Here we are just changing the prompts
- Fine-tuning approach: We would use a LoRA/QLoRA on a small labeled set (dozens to hundreds of examples) to adapt the model to your specific ticket style/categories. Much lighter than pre-training.
- When to fine-tune: When prompt-only accuracy isn't good enough, when you need consistent output format, or when latency/cost of a large model is too high and you want a smaller specialized one.


### Key differences
*Which "knobs" move between approaches? What is the equivalent of a training run in the LLMOps world?*

- Key knob that we turn is the prompt, because change in prompt will change the output
- Instead of changing model weights, you change what information the model receives at inference time.
- Inference parameters like temperature, top_p, max_tokens, frequency_penalty
- "done iterating" when prompt changes no longer improve accuracy on your eval set, or when you hit your quality threshold. Same concept as early stopping, just applied to prompt iterations instead of gradient steps.

---

## 3. Evaluation

### MLOps
*What metrics? How is the eval set constructed? How do you know the model is good enough to ship?*

- Accuracy, Precision, Recall, F1 score, Confusion matrix etc
- What does the eval set look like? (A held-out labeled set, never seen during training)
- What does "good enough to ship" mean concretely? (e.g., F1 > 0.90 on the test set, confusion matrix shows no catastrophic misclassifications)
- When do you re-evaluate? (After every retrain)

### LLMOps
*Why doesn't accuracy alone work? What replaces or supplements it? How do you evaluate a free-text explanation alongside a classification label?*

- "Output format" — correct, this is format compliance. Does the model return valid JSON? Does it include all required fields?
- "Confidence quality" — good instinct, but explain why it's unreliable. An LLM can say "confidence: 0.95" and be completely wrong because it's not a calibrated probability, it's a
generated token.
- Is the category correct? (You can still measure accuracy on the label — that part works)
- Is the reason field faithful and not hallucinated?
- Does the output degrade silently? (No error thrown, but quality drops — you'd never know without checking)
- Non-determinism: the same ticket may get different answers on different calls


### Key differences (this is the Definition-of-Done question — answer it here)
*Why is "model accuracy" monitoring not enough for LLM systems, and what replaces it?*

- As mentioned above model accuracy alone is not enough for LLM's
- Other things that matter are
  - Is the output format correct ?
  - How is the confidence quality. A high model confidence does not mean it is right
  - The reason given by the model, is it true ?
  - Model outputs from different can change
  - Silent degradation — in MLOps, if the model breaks you usually get an error or a measurable accuracy drop. In LLMOps, the model can confidently return wrong, hallucinated, or
  off-format answers with no signal at all. You need active monitoring to catch it
  - What replaces accuracy : format compliance checks, faithfulness scoring (is the reason grounded?), LLM-as-judge (using another LLM to rate outputs), and human
  spot-checks. Accuracy on the label still works, but it's just one of several signals now.

---

## 4. Deployment

### MLOps
*How is the model packaged and served? What does a model artifact look like (pickle, ONNX, TorchScript)? How do you roll back?*

- Usually the model will be converted into infernce based lighter frameworks like ONNX, TfLite, TensorRT, OpenVINO, Torch Script
- Model can be in model registry along with the config files that is required for inference.
- Model versioning helps in roll back
- How is it served? The model artifact gets loaded into a serving framework (e.g., FastAPI + ONNX runtime, TorchServe, Triton) and exposed as a REST endpoint. That's what
  "deployment" concretely means — the artifact running behind an API.
- What triggers a rollback? Accuracy drops below threshold on the monitoring set, or a regression is detected after a new model version is deployed. Rollback = swap the model
registry pointer back to the previous version and redeploy.

### LLMOps
*What is deployed? (Hint: the prompt is an artifact too.) How do you version and deploy a prompt change vs a model change? What does rollback mean when the model lives behind an API?*

- What is deployed, Common artifacts such as 
  - Prompt	(ticket_classifier_v7.txt)
  - Model	model=v3
  - Retrieval config	top_k=5
  - System instructions	system_prompt_v11
  - Output schema	json_schema_v4
  - Evaluation suite	eval_set_2026_06
  - Safety rules	guardrails_v2
- Different prompt versions
  - Prompt v1
  > Classify support tickets.
  - Prompt v2
  > Classify into:
    >
    > Billing
    >
    > Account
    >
    > Technical
- Typically it will be stored something like
    >prompts/
    >
    >ticket_classifier/
    >
    >v1.txt
    >
    >v2.txt

- Rollback — In LLMOps: rollback = swap the prompt file pointer back to the previous version (e.g., v1.txt instead of v2.txt) and redeploy your app. No model retraining, no artifact rebuild — just a config change. That's much faster than MLOps rollback.
- Model version changes — when Anthropic deprecates claude-sonnet-4-5 and you move to claude-sonnet-4-6, that's a deployment event too. You need to re-run your eval suite against the new model before promoting it, because behavior can change even with the same prompt.


### Key differences
*What new artifact types are introduced? What new deployment risks appear (latency, cost, non-determinism)?*

- As mentioned above apart from model artifact there are other artifact introduced in LLMOps like prompt, retrival config, system instruction, output schema etc
- Cost: every API call is billed per token, so a prompt change that adds 200 tokens multiplies across millions of requests — cost can spike silently without budget alerts.
- Latency: you're now dependent on an external network call; p95 latency is much harder to control than with a locally-served model.
- Non-determinism: the same input can return different outputs across calls (unless temperature=0), which makes regression testing harder — you can't just diff outputs

---

## 5. Monitoring

### MLOps
*What signals do you watch in production? What triggers a retraining run? What does "model drift" look like?*

- Data / Input signals (data drift)
  - You monitor whether incoming data has changed.
- Prediction signals (model behavior drift)
  - You monitor what the model is predicting.
- Ground truth / performance signals
  - If labels are available later:
    - accuracy
    - precision / recall
    - F1 score
    - ROC-AUC
    - log loss
- System signals (infra + reliability)
  - latency (P50 / P95 / P99)
  - error rate
  - timeouts
  - throughput (QPS)
  - resource usage
- Accuracy drop triggers model retrain
- What does drift actually look like concretely? For example: input tickets start containing a new product line's terminology the model never saw in training — prediction
  confidence drops, error rate on that slice rises. Or: the distribution of predicted categories shifts (suddenly 60% "Technical" where it used to be 30%) without a known cause.
  That's drift.
- What triggers a retrain? Name the threshold — e.g., F1 drops below 0.85 on a weekly labeled sample, or data drift score (PSI, KL divergence) exceeds a threshold. Monitoring is
only useful if it's wired to an action.


### LLMOps
*What signals replace or supplement accuracy metrics? Think about: output quality, cost, latency, hallucination rate, user feedback, guardrail trips.*

- Output quality (without ground truth)
  - Format compliance rate — what % of responses return valid JSON with all required fields. Easy to measure automatically on every call.
  - LLM-as-judge — a separate LLM call that scores the output for faithfulness, relevance, and tone. No human needed, runs async.
  - User feedback signals — thumbs up/down, escalation rate, re-submission rate. Indirect but highly reliable.

- Cost & latency
  - Token count per request (input + output) — a prompt change that inflates token count shows up immediately.
  - P50/P95 latency per request.
  - Cost per request and total daily spend. Alert when either exceeds a threshold.

- Guardrail trips
  - Rate at which requests are blocked or rewritten by guardrails. A sudden spike means either the input distribution shifted or the guardrail is misconfigured.

LLM drift (the hard one)
- Unlike MLOps, you don't own the model — Anthropic can silently update it. Monitor a golden set: a fixed set of inputs where you know the expected output. Run it daily and alert
if outputs change. That's your canary for model-side drift.
- Also watch category distribution shifts in predictions — if "Technical" jumps from 30% to 60% with no known cause, something changed

### Key differences
*What is "LLM drift" and how would you detect it? What is unique about monitoring non-deterministic, free-text outputs?*

- With updates on Anthropic side, drift can happen because of that. We need to have a golden set, so that we can run the model on that set and measure the drift
- Monitoring non-deterministic free-text outputs
  - Exact diffs stop working
  - Semantic equivalence becomes more important than lexical equivalence
    - embedding similarity
    - entailment scoring
    - semantic matching
    - LLM-as-judge
  - Variance itself becomes a production signal
    - output entropy
    - agreement rate
    - answer diversity

---

## Summary: What Stays the Same, What Changes

| Lifecycle Stage | MLOps | LLMOps | Biggest change |
|---|---|---|---|
| Data |Thousands of labeled (text,label) pairs; TF-IDF/embeddings; versioned in a data store. |Zero labels to start; the prompt encodes the schema; labels return only for an eval set. | Labeled data: prerequisite → optional eval asset.|
| Training / tuning | Real loop: embed → fit → minimize loss; stop on early-stopping/F1; mins to GPU-hours.| No training — iterate the prompt; optional LoRA/QLoRA on a small set.| Tune the prompt + temperature, not the weights.|
| Evaluation | Accuracy/precision/recall/F1 + confusion matrix on a held-out set.|Label accuracy plus format, faithfulness, calibration; LLM-as-judge + human checks. | “Good” goes from one number to many.|
| Deployment | Ship ONNX/TorchScript behind REST; roll back = registry pointer.| Ship prompt + model-id + schema + guardrails; roll back = swap a file.| New artifacts; cost, latency & non-determinism risks.|
| Monitoring |Data/prediction drift, F1, infra metrics; retrain on threshold. |Format %, judge scores, cost, guardrails + a golden set canary. |“LLM drift”: a model you don’t own can move. |

*Fill in the table last — it should flow naturally from the sections above.*

---

## One-Paragraph Takeaway

*After filling everything in: write 3-5 sentences summarizing the mental model shift from MLOps to LLMOps. This is what you'd say to a peer in a hallway conversation.*

- Going from MLOps to LLMOps moves the center of gravity from weights to prompts: instead of collecting and labeling data to train a model, you ship a prompt on day one and treat it as a versioned, reviewable artifact. Labeled data doesn’t vanish — it relocates from training fuel to an eval set. The hard part shifts downstream to evaluation and monitoring, because the model can be confidently wrong, hallucinated, or off-format with no error thrown, and the same input can vary call to call. And since you no longer own the model, a vendor update can cause silent drift you only catch with a golden set. Net: far less time training, far more spent on prompt iteration, output validation, and watching for failures that never raise an exception.
