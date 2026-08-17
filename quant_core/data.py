"""
OHLCV ingestion for a small ticker universe.

Keep this to daily bars, not intraday: the model in model.py is sized
for a laptop CPU, and richer data than the model can use doesn't buy
you anything but slower iteration.
"""
from datetime import date

import pandas as pd


def fetch_ohlcv(tickers: list[str], start: date, end: date) -> pd.DataFrame:
    """TODO: pull daily OHLCV for `tickers` (e.g. via yfinance).

    Keep the universe small (10-15 tickers) — this is a systems and
    modeling project, not a broad-market backtest.
    """
    raise NotImplementedError


def store_ohlcv(conn, ticker: str, df: pd.DataFrame) -> None:
    """Upsert OHLCV rows for `ticker`. `df` needs columns:
    date, open, high, low, close, volume."""
    rows = [
        (ticker, str(row.date), row.open, row.high, row.low, row.close, row.volume)
        for row in df.itertuples()
    ]
    conn.executemany(
        """INSERT OR REPLACE INTO ohlcv (ticker, date, open, high, low, close, volume)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def load_ohlcv(conn, ticker: str, start: date, end: date) -> pd.DataFrame:
    """Read back what's already stored, instead of re-fetching from
    the network every run — the whole point of persisting it locally."""
    return pd.read_sql_query(
        """SELECT date, open, high, low, close, volume FROM ohlcv
           WHERE ticker = ? AND date BETWEEN ? AND ? ORDER BY date""",
        conn, params=(ticker, start.isoformat(), end.isoformat()),
    )
