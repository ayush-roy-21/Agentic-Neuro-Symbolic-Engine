"""
DE/PSO signal-weight tuning + KKT-constrained portfolio solve.

DE/PSO tunes a SMALL parameter set (how the model's forecast and the
Oracle's sentiment score combine into one trade signal) — not the
transformer's weights. Population-based search doesn't scale to that;
see docs/future-work.md.

The portfolio solve uses cvxpy. Its interior-point solver satisfies
KKT conditions (stationarity, primal/dual feasibility, complementary
slackness) at the optimum internally — that's the theoretical result
to cite in the report; nobody hand-derives a solver for this in practice.
"""
import numpy as np
from scipy.optimize import differential_evolution

import cvxpy as cp


def tune_signal_weights(fitness_fn, n_params: int = 3, popsize: int = 20, maxiter: int = 40):
    """Small search space by design — keeps every generation cheap
    even on a CPU-only laptop. `fitness_fn` should score one weight
    vector against historical backtest performance (lower = better,
    scipy minimizes)."""
    bounds = [(0.0, 1.0)] * n_params
    result = differential_evolution(fitness_fn, bounds, popsize=popsize, maxiter=maxiter)
    return result.x


def optimize_portfolio(expected_returns: np.ndarray, cov: np.ndarray, risk_limit: float) -> np.ndarray:
    """Markowitz-style: maximize expected return subject to a variance
    cap and a fully-invested, long-only constraint.

    expected_returns: shape (n,) — per-asset expected return
    cov: shape (n, n) — covariance matrix
    risk_limit: max allowed portfolio variance
    """
    n = len(expected_returns)
    w = cp.Variable(n)
    objective = cp.Maximize(expected_returns @ w)
    constraints = [
        cp.sum(w) == 1,
        w >= 0,
        cp.quad_form(w, cov) <= risk_limit,
    ]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    return w.value
