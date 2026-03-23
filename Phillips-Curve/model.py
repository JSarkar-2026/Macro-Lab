"""
WS/PS Labour Market & Phillips Curve Model Engine
==================================================

CORE Econ Unit 4 — exact formulation (Sections 4.4–4.9)
---------------------------------------------------------
Labour Market:
    WS curve:  w_ws(e) = b + γ·e        (upward-sloping in employment rate e)
    PS curve:  w_ps = 1/(1+μ)           (flat — firms' markup determines real wage)
    Equilibrium: gap = 0  →  e* = (w_ps − b)/γ  →  u_n = (1 − e*) × 100

Bargaining Gap (CORE Section 4.5 — normalized fraction):
    gap_t = (w_ws(e_t) − w_ps) / w_ps

    Evaluated at the CURRENT employment level e_t.
    Positive gap: e > e* → workers demand more than firms can pay → inflationary.
    Negative gap: e < e* → slack → disinflationary.
    Multiply by 100 for percentage-point inflation impact.

Inflation equation (CORE Section 4.6 + asymmetric extension):
    π_t = π_t^e + α · scale · gap_t × 100 + ε_t

    scale = 1.0  if gap_t ≥ 0  (positive BG — full pass-through)
          = β    if gap_t < 0  (negative BG — dampened by downward wage rigidity)
    α = 1 is the CORE baseline.  β < 1 gives the empirical PC curvature.

Adaptive Expectations (CORE Section 4.6 — λ = 1 default):
    π_t^e = π_{t−1}^e + λ·(π_{t−1} − π_{t−1}^e)
    At λ = 1:  π_t^e = π_{t−1}

Rational Expectations:
    π_t^e = π*  (agents fully trust the CB target)

Central Bank Reaction (Section 4.9 narrative, formalised):
    u_t = u_n + φ · max(0, π_t^e − π*)
    Stability condition (WS/PS mode): α · γ · φ / w_ps < 1

WS/PS Structural Shocks:
    Δb   — permanent shift of the WS intercept from t=1 (e.g., benefit changes)
    Δμ   — permanent shift of the markup from t=1 (e.g., oil price shock)
    Both change the post-shock equilibrium: e*₁ = (w_ps_post − (b+Δb)) / γ

Period 0 — pre-shock steady state:
    e = e*₀, u = u_n_pre, gap = 0, π = π^e = π_e_init.
    True equilibrium when π_e_init = π*.

Period 1+ — post-shock dynamics:
    WS/PS shifts take effect.  CB reacts.  Economy adjusts to new equilibrium.

Standard Mode (γ = 0):
    π_t = π_t^e − α·(u_t − u_n) + ε_t;   Stability: α·φ < 1.

Reference: CORE-Econ 2.0 Unit 4; Sargent (1983); Lucas (1976).
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Literal


@dataclass
class ModelParams:
    """Parameters controlling the WS/PS Labour Market & Phillips Curve simulation."""

    alpha: float = 1.0
    """BG pass-through α.  α=1 (CORE baseline): 1% BG → 1 pp inflation above π^e."""

    u_n: float = 5.0
    """Natural unemployment rate (standard mode only; overridden by WS/PS equilibrium when γ>0)."""

    pi_star: float = 2.0
    """Central bank inflation target π* (%)."""

    pi_e_init: float = 2.0
    """
    Initial inflation expectations π_0^e (%).
    Default = π*: the economy starts in true equilibrium (BG=0, flat dynamics).
    Raise above π* to simulate the Sargent/inherited-inflation scenario.
    """

    lambda_adapt: float = 1.0
    """
    Adaptive expectations learning rate λ ∈ [0, 1].
    λ = 1 (CORE default): π_t^e = π_{t−1}.
    λ = 0: static expectations (never update).
    """

    phi: float = 0.8
    """
    CB aggressiveness φ.  u_t = u_n + φ · max(0, π_t^e − π*).
    Stability: α·γ·φ / w_ps < 1  (WS/PS mode).
    """

    n_periods: int = 20
    """Number of simulation periods T."""

    expectations: Literal["adaptive", "rational"] = "adaptive"
    """Expectations formation mechanism."""

    # ── WS/PS baseline parameters ─────────────────────────────────────────────
    b: float = 0.3
    """WS intercept b — workers' outside option / subsistence real wage."""

    gamma: float = 0.5
    """WS slope γ.  γ > 0 activates WS/PS mode."""

    mu: float = 0.3
    """Firm markup μ.  PS real wage: w_ps = 1/(1+μ)."""

    beta: float = 0.5
    """
    Downward wage-rigidity coefficient β ∈ (0, 1].
    Positive BG: scale = 1.0 (full pass-through).
    Negative BG: scale = β  (dampened — nominal wages resist cuts).
    β = 1: symmetric SRPC.  β < 1: empirical convex curvature.
    """

    # ── Structural shocks (permanent, from t=1) ────────────────────────────────
    delta_b: float = 0.0
    """
    WS intercept shift Δb (permanent from t=1).
    +Δb: WS shifts up → positive BG at original e*₀ → wage-push inflation.
    −Δb: WS shifts down → negative BG → disinflation.
    """

    delta_mu: float = 0.0
    """
    Markup shift Δμ (permanent from t=1 — e.g., oil price shock).
    +Δμ: PS shifts down → positive BG at original e*₀ → stagflation.
    −Δμ: PS shifts up → negative BG → disinflationary.
    """

    delta_AD_u: float = 0.0
    """
    Aggregate-demand shock in unemployment pp (permanent from t=1).
    Sign convention: POSITIVE = AD expansion (boom) — unemployment falls, employment
        rises above e*₀ → positive BG → economy moves ALONG the SRPC to higher inflation.
    Negative = AD contraction — unemployment rises, disinflation.
    Applied as: u_t = u_n_pre + φ·(π^e_t − π*) − delta_AD_u.
    """

    # ── Derived properties ────────────────────────────────────────────────────

    @property
    def use_bargaining_gap(self) -> bool:
        """True when WS/PS mode is active (gamma > 0)."""
        return self.gamma > 0.0

    @property
    def e_star(self) -> float:
        """Pre-shock labour market equilibrium e*₀.  Clamped to [0.01, 0.99]."""
        if not self.use_bargaining_gap:
            return 1.0 - self.u_n / 100.0
        w_ps = 1.0 / (1.0 + self.mu)
        return float(max(0.01, min(0.99, (w_ps - self.b) / self.gamma)))

    @property
    def u_n_derived(self) -> float:
        """Pre-shock natural unemployment rate u_n0."""
        if not self.use_bargaining_gap:
            return self.u_n
        return (1.0 - self.e_star) * 100.0

    @property
    def e_star_post(self) -> float:
        """Post-shock labour market equilibrium e*₁ (after Δb and Δμ take effect)."""
        if not self.use_bargaining_gap:
            return self.e_star
        b_post  = self.b  + self.delta_b
        mu_post = self.mu + self.delta_mu
        w_ps_post = 1.0 / (1.0 + mu_post) if (1.0 + mu_post) > 0 else 0.001
        return float(max(0.01, min(0.99, (w_ps_post - b_post) / self.gamma)))

    @property
    def u_n_post(self) -> float:
        """Post-shock natural unemployment rate u_n1 (the new long-run equilibrium)."""
        if not self.use_bargaining_gap:
            return self.u_n_derived
        return (1.0 - self.e_star_post) * 100.0


class PhillipsCurve:
    """
    WS/PS Labour Market & Phillips Curve simulation engine.

    Implements CORE Econ Unit 4 exactly, with a permanent structural shock
    mechanism (Δb, Δμ) for WS/PS curve shifts.

    Usage
    -----
    >>> p = ModelParams(pi_e_init=2.0, pi_star=2.0, delta_mu=0.1)
    >>> m = PhillipsCurve(p)
    >>> df = m.simulate()
    """

    def __init__(self, params: ModelParams) -> None:
        self.p = params

    # ------------------------------------------------------------------
    # Pre-shock curve methods
    # ------------------------------------------------------------------

    def ps_level(self) -> float:
        """Pre-shock PS real wage: w_ps = 1/(1+μ)."""
        return 1.0 / (1.0 + self.p.mu)

    def ws_curve(self, e_range: np.ndarray) -> np.ndarray:
        """Pre-shock WS curve: w_ws(e) = b + γ·e."""
        return self.p.b + self.p.gamma * e_range

    def bargaining_gap(self, e: float) -> float:
        """Pre-shock BG (fraction): (w_ws(e) − w_ps) / w_ps."""
        w_ps = self.ps_level()
        return (self.p.b + self.p.gamma * e - w_ps) / w_ps

    # ------------------------------------------------------------------
    # Post-shock curve methods
    # ------------------------------------------------------------------

    def ps_level_post(self) -> float:
        """Post-shock PS real wage: 1/(1 + (μ + Δμ))."""
        mu_post = self.p.mu + self.p.delta_mu
        return 1.0 / (1.0 + mu_post) if (1.0 + mu_post) > 0 else 0.001

    def ws_curve_post(self, e_range: np.ndarray) -> np.ndarray:
        """Post-shock WS curve: (b + Δb) + γ·e."""
        return (self.p.b + self.p.delta_b) + self.p.gamma * e_range

    def bargaining_gap_post(self, e: float) -> float:
        """
        Post-shock BG at employment e (CORE normalized formula):
            gap_post = (w_ws_post(e) − w_ps_post) / w_ps_post

        This is the gap ACTIVE from t=1 onward.
        At the original e*₀, this gives the opening impulse from the structural shock.
        """
        w_ps = self.ps_level_post()
        w_ws = (self.p.b + self.p.delta_b) + self.p.gamma * e
        return (w_ws - w_ps) / w_ps

    # ------------------------------------------------------------------
    # SRPC in (u, π) space
    # ------------------------------------------------------------------

    def srpc_at(self, pi_e: float, u_range: np.ndarray, post: bool = False) -> np.ndarray:
        """
        SRPC in (u, π) space anchored at π^e.

        Derived from the BG mechanism:
            gap = γ·(e − e*) / w_ps  and  (e − e*) = −(u − u_n)/100
            → π = π^e − α·γ/w_ps · (u − u_n)

        With downward wage rigidity (β < 1) the SRPC is KINKED at u_n:
          u < u_n → positive BG side → slope = α·γ/w_ps
          u > u_n → negative BG side → slope = β·α·γ/w_ps

        Parameters
        ----------
        post : bool
            If False (default): uses pre-shock w_ps and u_n0 (for initial SRPC).
            If True:            uses post-shock w_ps_post and u_n1 (for final SRPC).
        """
        if post:
            u_n   = self.p.u_n_post
            w_ps  = self.ps_level_post()
        else:
            u_n   = self.p.u_n_derived
            w_ps  = self.ps_level()

        if self.p.use_bargaining_gap:
            slope_pos = self.p.alpha * self.p.gamma / w_ps
            slope_neg = self.p.beta  * self.p.alpha * self.p.gamma / w_ps
            slopes = np.where(u_range <= u_n, slope_pos, slope_neg)
            return pi_e - slopes * (u_range - u_n)
        else:
            return pi_e - self.p.alpha * (u_range - u_n)

    # ------------------------------------------------------------------
    # Simulation
    # ------------------------------------------------------------------

    def simulate(self) -> pd.DataFrame:
        """
        Run the full dynamic simulation.

        Period 0 — pre-shock steady state:
            Curves:  original WS (b, γ),  PS (μ).
            State:   e = e*₀,  u = u_n0,  gap = 0,  π = π^e = π_e_init.
            When π_e_init = π* the economy is in true equilibrium — completely flat.

        Period 1+ — post-shock dynamics:
            Curves:  shifted WS (b+Δb, γ),  PS (μ+Δμ).
            CB ref:  u_n1 = u_n_post  (new structural rate).
            BG:      gap_t = bargaining_gap_post(e_t)  (CORE formula, fraction).
            Inflation: π_t = π_e_t + α·scale·gap_t·100   (scale = β if gap < 0).
            Expectations: adaptive π_e_t = π_{t-1}^e + λ·(π_{t-1} − π_{t-1}^e)
                       or rational π_e_t = π*.

        Returns
        -------
        pd.DataFrame with columns: t, u, pi, pi_e, e, bg, w_ws, w_ps.
        (bg = normalized gap fraction; ×100 = percentage-point inflation impact.)
        """
        p             = self.p
        n             = p.n_periods
        u_n_pre       = p.u_n_derived           # pre-shock natural rate
        u_n_post_val  = p.u_n_post              # post-shock natural rate (CB reference)
        e_star_pre    = p.e_star                # pre-shock equilibrium employment
        w_ps_pre_val  = self.ps_level()         # pre-shock PS (for t=0 row)
        w_ps_post_val = self.ps_level_post()    # post-shock PS (for t≥1 rows)

        u        = np.empty(n)
        pi       = np.empty(n)
        pi_e     = np.empty(n)
        e        = np.empty(n)
        bg       = np.empty(n)
        w_ws_arr = np.empty(n)
        w_ps_arr = np.empty(n)

        def _step(t_idx: int, pie_t: float) -> None:
            """
            One period t ≥ 1 using post-shock WS/PS.

            CB:   u_t = u_n_pre + φ · (π_e_t − π*)
                  The CB uses the PRE-SHOCK natural rate as its reference.
                  This correctly models a supply shock: when a WS/PS shift raises
                  the structural unemployment rate, the CB initially does not know
                  the new natural rate. It therefore reacts to inflation deviations
                  from target while anchoring at the OLD u_n. This is why inflation
                  rises persistently after a supply shock (the CORE stagflation story).
            BG:   gap_t = (w_ws_post(e_t) − w_ps_post) / w_ps_post
            π_t:  π_e_t + α · scale · gap_t · 100
            """
            u_t = max(0.01, min(30.0, u_n_pre + p.phi * (pie_t - p.pi_star) - 2.0 * p.delta_AD_u))
            e_t = max(0.01, min(0.99, 1.0 - u_t / 100.0))
            if p.use_bargaining_gap:
                gap_t = self.bargaining_gap_post(e_t)
                scale = 1.0 if gap_t >= 0.0 else p.beta
                pi_t  = pie_t + p.alpha * scale * gap_t * 100.0
            else:
                gap_t = 0.0
                pi_t  = pie_t - p.alpha * (u_t - u_n_pre)
            u[t_idx]        = u_t
            e[t_idx]        = e_t
            bg[t_idx]       = gap_t
            pi[t_idx]       = pi_t
            w_ws_arr[t_idx] = (p.b + p.delta_b) + p.gamma * e_t
            w_ps_arr[t_idx] = w_ps_post_val

        # ── Period 0: pre-shock steady state ──────────────────────────────────
        pi_e[0]     = p.pi_e_init
        u[0]        = u_n_pre
        e[0]        = e_star_pre
        bg[0]       = 0.0
        pi[0]       = p.pi_e_init
        w_ws_arr[0] = p.b + p.gamma * e_star_pre
        w_ps_arr[0] = w_ps_pre_val

        # ── Periods 1 … N−1: post-shock dynamics ──────────────────────────────
        for t in range(1, n):
            if p.expectations == "adaptive":
                pi_e[t] = pi_e[t - 1] + p.lambda_adapt * (pi[t - 1] - pi_e[t - 1])
            else:
                pi_e[t] = p.pi_star
            _step(t, pi_e[t])

        return pd.DataFrame({
            "t":    np.arange(n),
            "u":    u,
            "pi":   pi,
            "pi_e": pi_e,
            "e":    e,
            "bg":   bg,
            "w_ws": w_ws_arr,
            "w_ps": w_ps_arr,
        })

    def srpc_in_e(self, pi_e: float, e_range: np.ndarray, post: bool = True) -> np.ndarray:
        """
        SRPC in (e, π) space — positively sloped.

        π(e) = π^e + α · scale · gap(e) · 100
        where gap(e) = (w_WS(e) − w_PS) / w_PS

        The curve is kinked at e* (where gap = 0):
          e > e*: positive BG (WS > PS) → scale = 1.0   (full pass-through)
          e < e*: negative BG (WS < PS) → scale = β     (downward wage rigidity)

        Parameters
        ----------
        post : bool
            True  → use post-shock parameters (b+Δb, μ+Δμ); kink at e*₁.
            False → use pre-shock parameters (b, μ);           kink at e*₀.
        """
        if post:
            b_eff  = self.p.b + self.p.delta_b
            mu_eff = self.p.mu + self.p.delta_mu
            w_ps   = 1.0 / (1.0 + mu_eff) if (1.0 + mu_eff) > 0 else 0.001
        else:
            b_eff = self.p.b
            w_ps  = self.ps_level()
        w_ws  = b_eff + self.p.gamma * e_range
        gap   = (w_ws - w_ps) / w_ps
        scale = np.where(gap >= 0.0, 1.0, self.p.beta)
        return pi_e + self.p.alpha * scale * gap * 100.0

    def srpc_family(self, n_curves: int = 6) -> list:
        """Family of SRPC curves from π* to π_e_init, using post-shock parameters."""
        u_range     = np.linspace(0.0, 16.0, 400)
        pi_e_levels = np.linspace(self.p.pi_star, self.p.pi_e_init, n_curves)
        return [
            {"pi_e": float(round(pe, 2)),
             "u":    u_range,
             "pi":   self.srpc_at(pe, u_range, post=True)}
            for pe in pi_e_levels
        ]
