"""
SDE-informed forecasting model.

Deliberately NOT a novel architecture from scratch — that's an open
research problem (see docs/future-work.md). Instead: compose torchsde's
differentiable SDE solvers with a small forecasting transformer, so the
model's dynamics are structured like GBM (dS = mu*S*dt + sigma*S*dW)
rather than left to learn arbitrary dynamics from nothing.

CPU sizing: 2-4 transformer layers, 64-128 hidden dim, 30-60 day
lookback window. Use torchsde.sdeint with a fixed-step Euler-Maruyama
method (not an adaptive solver) — trading numerical precision for
speed, which is the right call on a laptop and worth naming as a
deliberate choice in the report.
"""
import torch
import torch.nn as nn


class DriftDiffusionNet(nn.Module):
    """Small MLPs parameterizing the SDE's drift (mu) and diffusion
    (sigma) terms. torchsde expects `noise_type`/`sde_type` attributes
    and f() / g() methods with this shape — check the current torchsde
    docs before wiring this up, this is a starting shape, not verified
    against a live install."""

    noise_type = "diagonal"
    sde_type = "ito"

    def __init__(self, hidden_dim: int = 64):
        super().__init__()
        self.drift_net = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, hidden_dim)
        )
        self.diffusion_net = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, hidden_dim), nn.Softplus()
        )

    def f(self, t: float, y: torch.Tensor) -> torch.Tensor:  # drift
        return self.drift_net(y)

    def g(self, t: float, y: torch.Tensor) -> torch.Tensor:  # diffusion
        return self.diffusion_net(y)


class ForecastTransformer(nn.Module):
    """TODO: the forecasting transformer itself. Keep it small (2-4
    layers). Its final hidden state feeds DriftDiffusionNet as the
    initial condition for an SDE integration (via torchsde.sdeint),
    rather than predicting a point forecast directly."""

    def __init__(self, input_dim: int, hidden_dim: int = 64, n_layers: int = 3):
        super().__init__()
        raise NotImplementedError
