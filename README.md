# Agentic Neuro-Symbolic Financial Engine

A multi-agent trading-signal pipeline combining an SDE-informed transformer,
closed-form financial math (Black-Scholes, no-arbitrage checks), evolutionary
optimization, and KKT-constrained portfolio risk limits — with a Rust/WASM
execution layer as a systems-engineering stretch goal.

## Structure & ownership

| Path | Contains | Owner |
|---|---|---|
| `quant_core/` | data, pricing, SDE-informed model, DE/PSO + KKT optimization | you — Math & Computing |
| `execution_engine/` | Rust order-matching core, compiled to WASM | you |
| `agents/` | Oracle, Risk, and the orchestration pipeline | your friend — CSE |
| `dashboard/` | Streamlit visualization | your friend |
| `schemas/` | shared message contracts (in-memory) | **both** — joint decision |
| `storage/` | shared SQLite schema (on-disk) — one local DB for documents + OHLCV | **both** — joint decision |

## Data sources

- **News**: Alpha Vantage's News & Sentiment endpoint has a genuine free tier and returns raw article text/metadata, not just a score. Use the raw text as input to your *own* Oracle pipeline (`embed_documents` → `analyze_sentiment`) — piping through Alpha Vantage's own precomputed sentiment score instead would bypass the actual assignment.
- **Filings**: SEC EDGAR's full-text search API (`efts.sec.gov/LATEST/search-index`) is free, needs no API key, and covers filings back to 2001. Send a descriptive `User-Agent` header and stay under 10 requests/second (SEC's fair-access policy) — that's the only real constraint.
- Neither free tier gives you years of deep historical *news* — EDGAR's 2001+ coverage is the stronger lever for building a historical backtest corpus; treat news history as thinner and plan the backtest accordingly.

The split follows your existing strengths: the stochastic-math and Rust/WASM
pieces sit with the Math & Computing background (the latter builds directly
on the EigenVM work); the agent orchestration, NLP pipeline, and dashboard
sit with the CSE-generalist track. `schemas/messages.py` is the one surface
both of you build against — agree on it in week 1, before writing code that
depends on it. If either of you wants to swap a piece based on actual
interest or a skill I don't know about, the boundary is just a suggestion,
not a constraint — the schema is what actually has to hold.

## Setup

```bash
pip install -r requirements.txt
cd execution_engine && cargo build
```

## Rough timeline (14–16 weeks)

- **Weeks 1–2** — You: OHLCV data pipeline. Friend: news/filings ingestion + embeddings.
- **Weeks 2–3** — You: Black-Scholes, Greeks, put-call parity checker.
- **Weeks 3–8** — You: SDE-informed transformer (small — 2–4 layers, CPU-sized). Friend: evidence-tier rubric + sentiment classification (weeks 3–6), then the Risk agent (weeks 6–9).
- **Weeks 9–10** — *Joint:* first crude end-to-end run — all pieces talking, nothing polished.
- **Weeks 9–13** — You: Rust matching engine → WASM demo → native/Python bridge. Friend: dashboard.
- **Weeks 13–14** — You: attention + Integrated Gradients on the transformer. Friend: SHAP on the sentiment classifier only.
- **Weeks 14–16** — *Joint:* full integration, evaluation, report, buffer.

See `docs/future-work.md` for what's deliberately out of scope, and why —
worth lifting close to verbatim into the report.
