"""
News/filings ingestion, embeddings, and evidence-graded sentiment tiers.

Use e5-base-v2 for embeddings — CPU inference is fine as long as you
embed once and cache to disk; never recompute for a document you've
already seen. Use an API call for the actual sentiment classification
rather than a local LLM — running an LLM repeatedly on CPU is the
slowest possible way to do this, and it's the one piece of the whole
project that doesn't need to touch your laptop's compute at all.
"""
from datetime import datetime

import numpy as np

from schemas.messages import EvidenceTier, OracleOutput
from storage.db import get_connection  # noqa: F401 -- re-exported for callers


def embed_documents(texts: list[str]):
    """TODO: sentence-transformers, model='intfloat/e5-base-v2'.
    Cache embeddings keyed by a hash of the source text."""
    raise NotImplementedError


def score_evidence_tier(source_type: str, corroborating_count: int, age_hours: float) -> EvidenceTier:
    """TODO: turn (source type x corroboration count x recency) into a
    tier. Write the actual thresholds down explicitly in this
    docstring once decided — that's what makes 'evidence-graded' a
    real, demoable rubric instead of a vague claim in the proposal."""
    raise NotImplementedError


def analyze_sentiment(ticker: str, texts: list[str], sources: list[dict]) -> OracleOutput:
    """TODO: call an LLM API for stance/sentiment classification,
    combine with score_evidence_tier, and return a populated
    OracleOutput — including a short `rationale` string, since that
    feeds the audit trail downstream."""
    raise NotImplementedError


def store_document(
    conn, doc_id: str, source_type: str, source_name: str, url: str | None,
    tickers: list[str], published_at: datetime, raw_text: str | None,
    embedding: np.ndarray | None, sentiment_score: float | None, evidence_tier: str | None,
) -> None:
    """Insert one ingested document plus its ticker links. This is the
    write side of the live store — call it once per document, as each
    one is ingested, not in a big batch at the end."""
    conn.execute(
        """INSERT OR REPLACE INTO documents
           (doc_id, source_type, source_name, url, published_at, ingested_at,
            raw_text, embedding, sentiment_score, evidence_tier)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            doc_id, source_type, source_name, url, published_at.isoformat(),
            datetime.utcnow().isoformat(), raw_text,
            embedding.astype(np.float32).tobytes() if embedding is not None else None,
            sentiment_score, evidence_tier,
        ),
    )
    for ticker in tickers:
        conn.execute("INSERT OR IGNORE INTO document_tickers (doc_id, ticker) VALUES (?, ?)", (doc_id, ticker))
    conn.commit()


def find_corroborating(conn, embedding: np.ndarray, ticker: str, since: datetime, threshold: float = 0.85) -> int:
    """Count existing documents about `ticker` since `since` whose
    embedding is similar to `embedding` (cosine similarity > threshold)
    — i.e. likely covering the same underlying story. This is what
    corroboration_count in score_evidence_tier actually measures.

    Deliberately a linear scan, not FAISS or a vector database: the
    candidate set here is always small (one ticker, a short recent
    window), so a brute-force cosine-similarity pass is effectively
    instant — a vector index would be solving a problem this project
    doesn't have.
    """
    cur = conn.execute(
        """SELECT d.embedding FROM documents d
           JOIN document_tickers t ON d.doc_id = t.doc_id
           WHERE t.ticker = ? AND d.published_at >= ? AND d.embedding IS NOT NULL""",
        (ticker, since.isoformat()),
    )
    candidates = [np.frombuffer(row[0], dtype=np.float32) for row in cur.fetchall()]
    if not candidates:
        return 0
    matrix = np.stack(candidates)
    sims = matrix @ embedding / (np.linalg.norm(matrix, axis=1) * np.linalg.norm(embedding) + 1e-9)
    return int((sims > threshold).sum())
