"""
Shared SQLite schema for the project's local, incremental store: every
ingested document (news/filings — the "corpus", built up over time) and
every OHLCV bar. One local file, one schema module — both tracks import
from here rather than each inventing their own storage ad hoc.

This is deliberately NOT the same thing as a research corpus in the
batch-NLP sense (collect everything, then analyze the whole set). This
table is written to incrementally, a few rows at a time, as new
documents and bars arrive, and is read with narrow, indexed queries —
"documents about ticker X since yesterday" — not full-table scans.

For backtesting and evaluation specifically, you still want a fixed,
point-in-time corpus (the classic agri-food-project pattern) — build
that as a one-time historical backfill into these same tables, tagged
by a `backfill` source_name or a separate date-range export, rather
than as a second, parallel storage system.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "financial_engine.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,       -- 'news' | 'filing' | 'social'
    source_name TEXT,
    url TEXT,
    published_at TEXT NOT NULL,      -- ISO 8601
    ingested_at TEXT NOT NULL,       -- ISO 8601
    raw_text TEXT,
    embedding BLOB,                  -- float32 array, via .tobytes()
    sentiment_score REAL,
    evidence_tier TEXT,              -- 'high' | 'medium' | 'low'
    corroboration_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS document_tickers (
    doc_id TEXT NOT NULL REFERENCES documents(doc_id),
    ticker TEXT NOT NULL,
    PRIMARY KEY (doc_id, ticker)
);

CREATE INDEX IF NOT EXISTS idx_doc_tickers_ticker ON document_tickers(ticker);
CREATE INDEX IF NOT EXISTS idx_documents_published ON documents(published_at);

CREATE TABLE IF NOT EXISTS ohlcv (
    ticker TEXT NOT NULL,
    date TEXT NOT NULL,              -- ISO 8601 date
    open REAL, high REAL, low REAL, close REAL, volume INTEGER,
    PRIMARY KEY (ticker, date)
);
"""


def get_connection() -> sqlite3.Connection:
    """One local SQLite file for the whole project. Safe to call
    repeatedly — creates the file and tables on first use, otherwise
    just opens the existing one."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    return conn
