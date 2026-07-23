# Multi-Agent Educational Orchestrator

An AI tutor for **CS 7280: Network Science**, grounded strictly in Barabási's
*Network Science* textbook. Instead of handing students answers, it walks them up a
three-level hint ladder, verifies every hint against the source material before showing
it, and escalates to a human when it runs out of safe things to say.

Built as a **LangGraph** multi-agent pipeline (retrieval → hint → verification), served
through a **Gradio** chat UI, with retrieval-quality and hallucination evaluation
harnesses and full structured-log observability.

---

## Why it exists

A naive RAG chatbot will happily give away the answer and occasionally hallucinate one.
For a tutor, both are failure modes. This project is organized around two guarantees:

1. **Never reveal the answer.** Hints are delivered on a ladder — L1 nudge → L2 context →
   L3 scaffold — and the hint agent is guardrailed against stating solutions, completing
   proofs, or giving step-by-step derivations.
2. **Never show an unverified hint.** Every generated hint passes a verification agent
   (SelfCheckGPT + source-faithfulness) before the student sees it. Hints that fail the
   gate are refused, not shown.

---

## Architecture

The full diagram lives in [`docs/architecture.mmd`](docs/architecture.mmd). At a glance:

```
Ingestion (offline):  PDF → text → chunk → embed (bge-small-en-v1.5) → ChromaDB

Live turn (LangGraph StateGraph, agents/orchestrator.py):
  question ─▶ Retrieval agent ─▶ route ─┬─▶ Hint agent ─▶ Verification agent ─▶ gate ─┬─▶ hint shown
                                        │                                             └─▶ safe refusal
                                        └─▶ Stuck node ─▶ decompose to sub-question ─▶ escalate to human
```

### The agents

| Agent | File | Role |
|-------|------|------|
| **Retrieval** | `agents/hint_agent.py` (`transform_retrieve`, `narrow_down`) | Query-transform + semantic search over ChromaDB (`k=5`), then narrow to the top 3 passages above a relevance floor. |
| **Hint** | `agents/hint_agent.py` (`render_hint`, `decompose`) | Generates exactly one hint at the requested ladder level, grounded only in retrieved passages. Decomposes to a prerequisite sub-question when the ladder is exhausted. |
| **Verification** | `agents/verification_agent.py`, `agents/faithfulness.py` | SelfCheckGPT (N=4 samples, cached) for hallucination + source-faithfulness for grounding. Gates whether the hint is shown. |

### Verification gates

Different hint levels are held to different standards, because they assert different things:

- **L1 (nudge)** — intentionally vague, so SelfCheckGPT can't score it fairly. Gated on
  **source-faithfulness ≥ 0.5** (deterministic, temp=0).
- **L2/L3 (context / scaffold)** — assert factual content. Gated on **SelfCheckGPT
  hallucination ≤ 0.69**. Faithfulness is logged but not the gate here.

(See `agents/orchestrator.py` — `FAITHFULNESS_GATE`, `HALLUCINATION_THRESHOLD`.)

### Getting unstuck & human escalation

When a student is still stuck after L3, the **stuck node** decomposes the question into a
smaller prerequisite sub-question and restarts the ladder at L1. After
`MAX_STUCK_CYCLES` such cycles, the conversation is **escalated to a human** (post to Ed
Discussion) and locked — no further automated answers.

### Continuation-intent detection

`agents/intent.py` decides whether an incoming message means *"continue the current hint
ladder"* ("more", "keep going") or *"this is a new question"* (reset the ladder). It is
deterministic where it can be and calls the LLM only where it must be:

- empty / pure-punctuation → continue;
- otherwise score by cosine similarity to continuation-cue seeds using the **same
  bge-small-en-v1.5 encoder as retrieval** (reproducible, no LLM call);
- a **high** score is a confident continue, a **low** score a confident new question;
- only scores in the **ambiguous band** fall back to a temperature-0 LLM classifier.

---

## Evaluation

Retriever and verifier choices are backed by evaluation harnesses, not vibes.

- **Retriever choice — Plain RAG over HyDE.** On a labeled set of Network Science
  questions → relevant chapter (`evaluation/metrics.py`, `ACCURATE_DATA`), plain RAG beat
  HyDE on top-5 retrieval (**0.98 vs 0.93**) while being cheaper and deterministic (no LLM
  call in the retrieval path).
- **Hallucination detection.** SelfCheckGPT scoring reaches **PR-AUC ≈ 0.94** vs a 0.5
  baseline (`docs/eval_scores.json`, `docs/pr_curve.png`; harness in
  `evaluation/hallucination_eval.py`).

---

## Observability

Every turn emits a structured JSON log via `structlog` (`observability/log.py`,
`log_turn`) — verification decisions, decision reasons, scores, stuck/escalation events,
and **thumbs up/down feedback** from the UI (`event=feedback`). Logs are written to
`logs/conversation.jsonl` and shipped to a local **Grafana + Loki + Promtail** stack via
`docker-compose.yml`.

**Feedback:** clicking 👍 / 👎 on any hint in the chat UI logs an `event=feedback` turn
(with `liked`, `conversation_id`, `turn`, `hint`) into the same stream, so it's queryable
in Grafana alongside everything else.

---

## Setup

### 1. Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env    # then fill in your values
```

| Variable | Purpose |
|----------|---------|
| `GROQ_API_KEY` | LLM inference (hint generation, verification, intent fallback) |
| `CHROMA_PATH` | ChromaDB persistent directory (default `./data/chromadb`) |
| `TEXT_DIR` / `PDF_DIR` | Ingestion source paths |
| `REDIS_URL` | Cache for retrieval + SelfCheckGPT samples (default `redis://localhost:6379/0`) |
| `LOG_PATH` | Structured log output (default `./logs/conversation.jsonl`) |

### 3. Start dependencies (Redis, and optionally the observability stack)

```bash
docker compose up -d redis                     # required
docker compose up -d loki promtail grafana     # optional: Grafana at http://localhost:3001
```

### 4. Build the vector index (one-time ingestion)

```bash
python ingest/pdt_to_text.py    # PDF chapters → data/text/
python ingest/chunk.py          # chunk + embed → ChromaDB
```

### 5. Run the tutor

```bash
python app.py                   # Gradio UI
```

---

## Testing

```bash
pytest                          # run the suite
pytest --cov --cov-report=term  # with coverage (requires pytest-cov)
```

`tests/test_retrieval.py` covers the retrieval layer today.

---

## Project layout

```
app.py                      Gradio chat UI + session state + feedback logging
agents/
  orchestrator.py           LangGraph StateGraph: routing, gates, stuck/escalation
  hint_agent.py             Retrieval + hint ladder + decomposition
  verification_agent.py     SelfCheckGPT hallucination scoring
  faithfulness.py           Source-faithfulness scoring
  intent.py                 Continuation-vs-new-question detection
retrieval/                  basic_rag / hyde_rag / retriever
ingest/                     PDF → text → chunk → embed
evaluation/                 retrieval + hallucination eval harnesses
observability/              structlog config + Grafana/Loki/Promtail
cache/                      Redis JSON cache
docs/                       architecture diagram + eval artifacts
```
