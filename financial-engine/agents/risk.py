"""
Expected-utility check, constraint validation, and the audit trail.

Every decision this agent makes — approved or rejected — gets logged
with a rationale. That log IS your audit trail, and it's a genuinely
good interpretability artifact on its own: probably more convincing to
an examiner than a half-working SHAP integration would be.
"""
from schemas.messages import QuantSignal, RiskDecision


def check_constraints(signal: QuantSignal, portfolio_weights: dict[str, float]) -> RiskDecision:
    """TODO: validate the proposed trade against quant_core.optimize's
    KKT-constrained weights and an expected-utility bound. Always
    return a RiskDecision — approved or not — with a populated
    `rationale`, even (especially) on rejection."""
    raise NotImplementedError
