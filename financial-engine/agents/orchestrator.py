"""
Wires Oracle -> Quant -> Risk together.

Deliberately plain message-passing instead of a heavyweight agent
framework (LangGraph, CrewAI, etc.) — a 3-stage, mostly-linear pipeline
doesn't need one, and hand-rolled orchestration is easier to defend
when someone asks exactly what happens at each step.
"""
from schemas.messages import RiskDecision


def run_pipeline(ticker: str) -> RiskDecision:
    """TODO:
      1. agents.oracle.analyze_sentiment(ticker, ...)      -> OracleOutput
      2. quant_core.model forecast, fed the OracleOutput   -> QuantSignal
      3. agents.risk.check_constraints(signal, ...)        -> RiskDecision
    Log every intermediate message (not just the final decision) —
    that full trace is what makes the audit trail actually auditable.
    """
    raise NotImplementedError
