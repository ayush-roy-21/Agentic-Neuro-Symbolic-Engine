"""
Shared message schemas — the contract between quant_core, agents, and
execution_engine. Treat changes here as a decision both collaborators
make together; code on both sides of the project depends on these
shapes staying stable.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EvidenceTier(str, Enum):
    """How well-corroborated an Oracle sentiment read is."""

    HIGH = "high"      # multiple primary sources, recent
    MEDIUM = "medium"  # one primary source, or multiple secondary
    LOW = "low"        # single secondary/unverified source


class OracleOutput(BaseModel):
    """Emitted by the Oracle agent for one ticker, per ingestion cycle."""

    ticker: str
    timestamp: datetime
    sentiment_score: float = Field(ge=-1.0, le=1.0)
    evidence_tier: EvidenceTier
    source_count: int
    rationale: str  # short, human-readable — feeds the audit trail


class QuantSignal(BaseModel):
    """Emitted by the Quant agent — a candidate trade, not yet risk-checked."""

    ticker: str
    timestamp: datetime
    forecast_drift: float  # model's estimated mu
    forecast_vol: float    # model's estimated sigma
    raw_signal: float = Field(ge=-1.0, le=1.0)  # -1 full sell .. +1 full buy
    oracle_input: OracleOutput | None = None


class RiskDecision(BaseModel):
    """Emitted by the Risk agent — the final, auditable decision."""

    ticker: str
    timestamp: datetime
    approved: bool
    final_weight: float | None = None  # portfolio weight, if approved
    constraint_violations: list[str] = Field(default_factory=list)
    rationale: str
    upstream_signal: QuantSignal
