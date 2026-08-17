"""
Black-Scholes, the Greeks, and a no-arbitrage check.

This is the most tractable module in the project: closed-form, no
iterative solving, a few days of work done properly. Treat it as your
early, reliable win.
"""
import math

from scipy.stats import norm


def _d1_d2(S: float, K: float, T: float, r: float, sigma: float) -> tuple[float, float]:
    d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return d1, d2


def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """European call price. S=spot, K=strike, T=years to expiry,
    r=risk-free rate, sigma=volatility."""
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def black_scholes_put(S: float, K: float, T: float, r: float, sigma: float) -> float:
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def greeks(S: float, K: float, T: float, r: float, sigma: float) -> dict:
    """TODO: delta, gamma, vega, theta, rho. Delta and gamma are the
    ones the Risk agent actually needs for constraint checks — start
    there before filling in the rest."""
    raise NotImplementedError


def put_call_parity_violation(call_price: float, put_price: float, S: float, K: float, T: float, r: float) -> float:
    """Returns C - P - (S - K*e^-rT). Non-zero beyond a small
    transaction-cost tolerance flags a potential arbitrage — this
    is the 'arbitrage theorem', operationalized as something checkable."""
    return call_price - put_price - (S - K * math.exp(-r * T))
