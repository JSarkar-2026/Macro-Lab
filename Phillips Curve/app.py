"""
WS/PS Labour Market & Phillips Curve Interactive Simulation — Animated
======================================================================
Streamlit app demonstrating:
  · Bargaining Gap model (WS/PS Labour Market)
  · Inflation expectations, Bargaining Gap & Phillips Curve dynamics
  · Adaptive vs. Rational Expectations
  · The Lucas Critique and Sacrifice Ratio

Run locally:  streamlit run app.py
Deploy:       Streamlit Community Cloud
"""

import hashlib
import random
import time

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from model import ModelParams, PhillipsCurve

# ─────────────────────────────────────────────────────────────────────────────
# 0. Page configuration
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WS/PS Labour Market & Phillips Curve | Macroeconomics Lab",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Google Analytics
# ─────────────────────────────────────────────────────────────────────────────
GA_ID = "G-XXXXXXXXXX"
st.markdown(
    f"""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_ID}');
    </script>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Custom CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f1f5f9; }

    /* Main content — force dark text regardless of system theme */
    [data-testid="stMainBlockContainer"],
    [data-testid="stMainBlockContainer"] p,
    [data-testid="stMainBlockContainer"] li,
    [data-testid="stMainBlockContainer"] span,
    [data-testid="stMainBlockContainer"] label,
    [data-testid="stMarkdown"] p,
    [data-testid="stMarkdown"] li,
    [data-testid="stMarkdown"] h3,
    [data-testid="stMarkdown"] h4,
    .stExpander [data-testid="stMarkdown"] p,
    .stExpander [data-testid="stMarkdown"] li,
    .element-container p,
    .stAlert p,
    .stCaption p                        { color: #1e293b !important; }

    /* Sidebar */
    [data-testid="stSidebar"]           { background-color: #1e293b; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3         { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stCaption p { color: #94a3b8 !important; font-size: 0.78rem !important; }

    /* Primary buttons — white text on indigo */
    button[kind="primary"],
    button[kind="primary"] p,
    button[kind="primary"] span          { color: #ffffff !important; }

    /* Page header banner */
    .lab-header {
        background: linear-gradient(135deg, #1e293b 0%, #312e81 100%);
        padding: 2rem 2.5rem 1.6rem;
        border-radius: 0 0 16px 16px;
        margin-bottom: 1.2rem;
    }
    .lab-header h1,
    .lab-header h1 span,
    .lab-header h1 p   { font-family: Georgia, "Times New Roman", serif;
                         font-size: 1.9rem; font-weight: 700;
                         color: #ffffff !important; margin: 0; }
    .lab-header p,
    .lab-header p span { color: #a5b4fc !important; margin: 0.3rem 0 0; font-size: 0.95rem; }

    /* Section headers */
    .section-h { font-family: Georgia, serif; color: #1e293b !important;
                 border-bottom: 2px solid #e0e7ff; padding-bottom: 0.3rem; }

    /* Metric boxes */
    [data-testid="metric-container"] {
        background: #ffffff; border-radius: 10px;
        padding: 0.6rem 0.9rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    }

    /* Tab indicator */
    .stTabs [aria-selected="true"] { color: #4338ca !important; border-bottom-color: #4338ca !important; }

    /* Status box */
    .status-box {
        background: #f8fafc; border-left: 4px solid #4338ca;
        border-radius: 0 8px 8px 0; padding: 0.7rem 1.2rem;
        margin: 0.5rem 0 1rem; font-size: 0.95rem; color: #1e293b;
    }

    /* Animation period badge */
    .period-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4338ca, #6d28d9);
        color: white !important; border-radius: 20px; padding: 0.35rem 1.2rem;
        font-size: 1.05rem; font-weight: bold; font-family: Georgia, serif;
        margin: 0.25rem 0;
    }

    /* Quiz question card */
    .quiz-q {
        background: #ffffff; border-left: 4px solid #4338ca;
        border-radius: 0 8px 8px 0; padding: 0.9rem 1.4rem 0.8rem;
        margin-bottom: 0.8rem; box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    }
    .quiz-q h4 { color: #1e293b; font-family: Georgia, serif;
                 margin-bottom: 0.3rem; font-size: 1.05rem; }

    /* Quiz feedback cards */
    .quiz-correct {
        background: #f0fdf4; border-left: 4px solid #16a34a;
        border-radius: 0 8px 8px 0; padding: 0.65rem 1.1rem;
        margin: 0.3rem 0 0.4rem; font-size: 0.94rem; color: #166534;
    }
    .quiz-wrong {
        background: #fef2f2; border-left: 4px solid #ef4444;
        border-radius: 0 8px 8px 0; padding: 0.65rem 1.1rem;
        margin: 0.3rem 0 0.2rem; font-size: 0.94rem; color: #991b1b;
    }
    .quiz-answer-correct {
        background: #f0fdf4; border-left: 4px solid #16a34a;
        border-radius: 0 8px 8px 0; padding: 0.55rem 1.1rem;
        margin: 0.2rem 0 0.4rem; font-size: 0.93rem; color: #166534;
    }
    .quiz-exp {
        background: #f0f4ff; border-left: 4px solid #818cf8;
        border-radius: 0 8px 8px 0; padding: 0.7rem 1.1rem;
        margin: 0.3rem 0 0.2rem; font-size: 0.92rem; color: #1e293b;
    }

    /* Score badge */
    .score-badge {
        background: linear-gradient(135deg, #4338ca, #6d28d9);
        color: #fff; border-radius: 12px; padding: 1rem 1.5rem;
        text-align: center; margin: 0.5rem 0 1rem;
        display: flex; align-items: center; justify-content: center; gap: 1.5rem;
    }
    .score-badge .big { font-size: 2rem; font-weight: bold;
                        font-family: Georgia, serif; color: #fff !important; }
    .score-badge .label { font-size: 0.9rem; color: #ddd6fe !important; }

    /* Copyright footer */
    .copyright-footer {
        text-align: center; color: #64748b; font-size: 0.8rem;
        padding: 1.5rem 0 0.5rem; border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }

    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Quiz data — 7 questions
# ─────────────────────────────────────────────────────────────────────────────
QUIZ: list[dict] = [
    {
        "q": "What does the Short-Run Phillips Curve (SRPC) illustrate?",
        "opts": [
            "The long-run relationship between money supply and real output",
            "The trade-off between inflation and unemployment for given inflation expectations",
            "The relationship between interest rates and investment spending",
            "The long-run supply-side growth potential of an economy",
        ],
        "ans": 1,
        "exp": (
            "The SRPC shows the inverse π–u relationship **conditional on a fixed π^e**. "
            "It is anchored at π^e when u = u_n and shifts vertically when expectations change."
        ),
    },
    {
        "q": "Why does the Short-Run Phillips Curve shift vertically?",
        "opts": [
            "Because the slope α changes with monetary tightening",
            "Because the natural rate u_n rises over time",
            "Because inflation expectations π^e change, re-anchoring the curve",
            "Because the money supply growth rate is adjusted by the central bank",
        ],
        "ans": 2,
        "exp": (
            "The SRPC is π = π^e − α(u − u_n). "
            "A change in π^e shifts the entire curve up or down by the same amount — a pure vertical shift."
        ),
    },
    {
        "q": "Under adaptive expectations, how do agents form their inflation forecast?",
        "opts": [
            "They use the central bank's announced target directly",
            "They use all available current information rationally",
            "They adjust last period's expectation toward last period's actual inflation",
            "They always expect the same inflation rate as in the steady state",
        ],
        "ans": 2,
        "exp": (
            "Adaptive expectations: π_t^e = π_{t-1}^e + λ(π_{t-1} − π_{t-1}^e). "
            "The standard adaptive case uses λ=1 so π_t^e = π_{t−1}: agents always expect last period's inflation. "
            "This creates sluggish adjustment and a costly sacrifice ratio."
        ),
    },
    {
        "q": "What is the Long-Run Phillips Curve (LRPC)?",
        "opts": [
            "A downward-sloping curve showing the permanent inflation-unemployment trade-off",
            "A vertical line at the natural rate of unemployment u_n",
            "A horizontal line at the central bank's inflation target π*",
            "An upward-sloping curve reflecting supply-side constraints",
        ],
        "ans": 1,
        "exp": (
            "In long-run equilibrium π = π^e, so the SRPC collapses to u = u_n. "
            "The LRPC is a **vertical line at u_n** — there is no permanent inflation-unemployment trade-off."
        ),
    },
    {
        "q": "The 'Lucas Critique' (1976) argues that:",
        "opts": [
            "Inflation is always and everywhere a monetary phenomenon",
            "Central banks cannot permanently reduce the unemployment rate",
            "Econometric models estimated under one policy regime become unreliable when the regime changes",
            "Rational expectations always produce lower output than adaptive expectations",
        ],
        "ans": 2,
        "exp": (
            "Lucas showed that forward-looking agents alter their behaviour when policy changes, "
            "invalidating historical relationships. The shifting SRPC is the textbook illustration."
        ),
    },
    {
        "q": "In the Bargaining Gap model, what causes the SRPC to shift upward even without a change in monetary policy?",
        "opts": [
            "The central bank raises its inflation target π*",
            "The slope α of the Phillips Curve increases",
            "Employment rises above the labour market equilibrium, opening a positive Bargaining Gap",
            "Agents switch from rational to adaptive expectations",
        ],
        "ans": 2,
        "exp": (
            "When e > e*, w_WS(e) > w_PS: workers bargain for a real wage above what firms can pay. "
            "Firms pass the cost into prices → actual inflation exceeds expected inflation. "
            "Rising actual inflation raises π^e next period → SRPC shifts up. "
            "This operates independently of any monetary policy change."
        ),
    },
    {
        "q": "What is the Price-Setting (PS) real wage, and why is it flat (horizontal)?",
        "opts": [
            "It is the real wage negotiated in collective bargaining agreements, rising with employment",
            "It equals 1/(1+μ), determined by the firm's markup over costs — independent of employment",
            "It is the real wage consistent with zero unemployment, rising with productivity",
            "It is the central bank's target real wage, held constant by policy",
        ],
        "ans": 1,
        "exp": (
            "The PS real wage is w_PS = 1/(1+μ), where μ is the firm's markup over unit labour costs. "
            "Because μ is set by product-market competition (not employment conditions), "
            "the PS curve is perfectly flat — firms' ability to pay a given real wage does not change "
            "as more or fewer workers are employed."
        ),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 4. Session-state defaults
# ─────────────────────────────────────────────────────────────────────────────
_defaults: dict = {
    "intro_complete":  False,  # True after the user clicks "Enter Simulation"
    "param_ver":       0,
    "anim_frame":      0,
    "anim_running":    False,
    "anim_t_max":      10,
    "last_param_hash": "",    # empty string = first load (no auto-play)
    "quiz_answers":    {},    # {orig_idx: selected_opt_idx}
    "quiz_order":      None,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

if st.session_state["quiz_order"] is None:
    _order = list(range(len(QUIZ)))
    random.shuffle(_order)
    st.session_state["quiz_order"] = _order

# ─────────────────────────────────────────────────────────────────────────────
# 5. Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="lab-header">
      <h1>📈 WS/PS Labour Market &amp; Phillips Curve Simulation</h1>
      <p>Macroeconomics Interactive Lab &nbsp;·&nbsp;
         Bargaining Gap, Expectations &amp; Inflation Dynamics</p>
    </div>
    """,
    unsafe_allow_html=True,
)

_home_col, _ = st.columns([1, 7])
with _home_col:
    if st.button("← Lab Home", use_container_width=True):
        try:
            st.switch_page("../app.py")
        except Exception:
            st.info("Lab home not found. Run standalone with `streamlit run app.py`.")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# 6. Welcome / How-to-run page (shown on first visit; hidden after "Enter")
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state["intro_complete"]:

    # ── Intro header ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#312e81 0%,#4338ca 100%);
                    border-radius:12px;padding:1.8rem 2.2rem 1.4rem;margin-bottom:1.4rem;">
          <h2 style="color:#ffffff;font-family:Georgia,serif;margin:0;font-size:1.6rem;">
            Welcome to the WS/PS Labour Market &amp; Phillips Curve Simulation
          </h2>
          <p style="color:#c7d2fe;margin:0.5rem 0 0;font-size:0.97rem;">
            An interactive tool for exploring how wages, prices, inflation expectations,
            and central bank policy interact in the macroeconomy.
            Read this page before starting — it takes about two minutes.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_left, col_mid, col_right = st.columns([5, 5, 4])

    with col_left:
        st.markdown("#### 🔬 What this simulation shows")
        st.markdown(
            "The model has three interacting parts:\n\n"
            "**1. WS/PS Labour Market** — Workers bargain over the real wage "
            "(upward-sloping WS curve). Firms set the highest real wage they can "
            "afford given their markup (flat PS line). "
            "Where WS = PS is the equilibrium employment rate **e\\*** and the "
            "natural unemployment rate **u_n**.\n\n"
            "**2. Bargaining Gap (BG)** — When employment is above e\\*, workers "
            "push wages above what firms planned. Firms raise prices. "
            "The BG drives inflation above expected inflation. "
            "A negative BG does the reverse, but wages are downwardly rigid — "
            "so disinflation is weaker than inflation for the same-sized gap "
            "(*asymmetric curvature* of the Phillips Curve).\n\n"
            "**3. Inflation Expectations & SRPC** — Expectations adapt with a "
            "one-period lag (adaptive) or jump immediately to the CB's target "
            "(rational). Each expectation update shifts the SRPC vertically, "
            "tracing the Long-Run Phillips Curve — a vertical line at u_n."
        )

        st.markdown("#### ▶ How the animation works")
        st.markdown(
            "**Shift any slider in the left panel** — the simulation "
            "immediately animates through up to 10 adjustment periods.\n\n"
            "- **φ = 0** (default): CB is fully accommodating. "
            "Animation always runs all 10 periods, showing how inflation "
            "spirals upward as expectations adapt.\n"
            "- **φ > 0** (CB active): Animation stops automatically when "
            "unemployment converges to the new natural rate — which may happen "
            "before period 10 for large φ or small shocks.\n\n"
            "Use the four buttons at the top of the Simulation tab to "
            "**▶ Play**, **⏸ Pause**, **⏮ Reset to t=0**, or jump to the "
            "**⏭ Final** period."
        )

    with col_mid:
        st.markdown("#### 📋 Six scenarios to try")
        st.markdown(
            "**1 — Stable baseline** *(no shock, φ = 0)*  \n"
            "Leave all sliders at defaults. BG = 0 everywhere. "
            "Nothing moves across all 10 periods — the model is in steady state.\n\n"
            "**2 — Markup shock (stagflation)**  \n"
            "Raise firm markup **μ** above 0.30 (try 0.45). "
            "The PS line shifts down. A positive BG opens at e\\*₀ → "
            "inflation accelerates. With φ = 0 it spirals indefinitely. "
            "Raise φ to see the CB tighten and unemployment rise toward new u_n₁.\n\n"
            "**3 — AD boom** *(movement along SRPC)*  \n"
            "Set AD demand shock to **+6**. Employment rises above e\\*₀. "
            "The WS/PS curves do NOT move — but BG > 0 opens at the new "
            "employment point. In period 1 the economy moves *along* the SRPC. "
            "From period 2, π^e adapts and the SRPC shifts upward.\n\n"
            "**4 — CB policy response**  \n"
            "With any shock active, raise **φ** (try 2.0–4.0). "
            "Higher φ → faster convergence toward u_n₁, at the cost of "
            "deeper short-run unemployment.\n\n"
            "**5 — Oil price shock**  \n"
            "Set Oil price shock to **+15%** (0.15). "
            "This raises the effective markup, PS shifts down — same "
            "stagflation as scenario 2, driven by commodity costs. "
            "A negative value simulates a favourable supply shock.\n\n"
            "**6 — Lucas Critique**  \n"
            "With any shock and φ > 0 active, switch **Expectations** to "
            "Rational. Agents immediately anticipate the CB's adjustment — "
            "the SRPC collapses in one step and disinflation is costless."
        )

    with col_right:
        st.markdown("#### ⚙️ Slider quick reference")
        st.markdown(
            "| Slider | Default | Effect |\n"
            "|--------|---------|--------|\n"
            "| WS intercept **b** | 0.30 | Higher → WS shifts up → higher u_n |\n"
            "| AD demand shock | 0 | Positive = boom; negative = slump |\n"
            "| Firm markup **μ** | 0.30 | Higher → PS shifts down → higher u_n |\n"
            "| Oil price shock | 0% | Same as markup shift |\n"
            "| Slope **α** | 0.10 | Steeper SRPC → faster inflation |\n"
            "| Inflation target **π\\*** | 2.0% | CB's goal |\n"
            "| Policy intensity **φ** | 0.0 | 0 = accommodating; raise to tighten |\n"
            "| Expectations | Adaptive | Switch to Rational for Lucas Critique |"
        )

        st.markdown("#### 📊 Reading the three panels")
        st.markdown(
            "**WS/PS diagram** — The coloured dot tracks the economy's "
            "employment position each period. The orange/purple bar is the "
            "current Bargaining Gap.\n\n"
            "**Phillips Curve (e, π)** — SRPC curves accumulate as "
            "expectations ratchet up. The amber dot marks the current period.\n\n"
            "**Time Series** — Inflation (actual and expected) top panel; "
            "unemployment vs. natural rate bottom panel. "
            "Dashed red line = u_n₀; dashed dark-red = u_n₁ after a supply shock."
        )

        st.markdown("#### 📝 Quiz tab")
        st.markdown(
            "The **Quiz** tab tests understanding of inflation expectations, "
            "the Bargaining Gap, and the Lucas Critique. "
            "Click any option button — immediate feedback appears. "
            "You can revisit it at any time alongside the simulation."
        )

    st.markdown("---")
    _enter_col, _ = st.columns([2, 6])
    with _enter_col:
        if st.button("▶ Enter Simulation", type="primary", use_container_width=True):
            st.session_state["intro_complete"] = True
            st.rerun()

    st.markdown(
        '<div class="copyright-footer">'
        '© Jayanta Sarkar (Queensland University of Technology, 2026) &nbsp;·&nbsp; '
        'WS/PS Labour Market &amp; Phillips Curve Simulation'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()   # do not render sidebar or simulation tabs on this page

# ─────────────────────────────────────────────────────────────────────────────
# 6. Fixed model constants
# ─────────────────────────────────────────────────────────────────────────────
_GAMMA  = 0.55   # WS slope γ
_BETA   = 0.5    # Downward wage-rigidity β (asymmetric PC curvature)
_LAMBDA = 1.0    # Adaptive expectations (λ=1): π_e_t = π_{t-1}
_B0     = 0.3    # Baseline WS intercept
_MU0    = 0.3    # Baseline firm markup
_W_PS0  = 1.0 / (1.0 + _MU0)
_E_STAR0 = float(max(0.01, min(0.99, (_W_PS0 - _B0) / _GAMMA)))
_U_N0   = (1.0 - _E_STAR0) * 100.0
_T_MAX  = 10     # maximum animation periods

# ─────────────────────────────────────────────────────────────────────────────
# 7. Sidebar — Model Parameters
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Model Parameters")
    _v = st.session_state["param_ver"]

    # ── Labour Market ───────────────────────────────────────────────────────
    st.markdown("### 🏭 Labour Market")
    b_ws = st.slider(
        "WS intercept b", 0.1, 0.6, 0.3, 0.05,
        key=f"bws_{_v}",
        help=(
            "Workers' outside option / unemployment benefit. "
            "Higher b → WS curve shifts up → lower e* → higher u_n."
        ),
    )
    delta_AD_u = st.slider(
        "AD demand shock", -10.0, 10.0, 0.0, 1.0,
        key=f"adu_{_v}",
        help=(
            "Aggregate demand shock, permanent from t=1. "
            "Positive: AD expansion (boom) — unemployment falls, employment rises "
            "above e*₀ → positive Bargaining Gap → economy moves ALONG the SRPC. "
            "Negative: AD contraction — unemployment rises, disinflation. "
            "Sets: u_t = u_n + φ·(π^e − π*) − Δ."
        ),
    )
    if abs(delta_AD_u) > 0.01:
        _e_ad_sb = max(0.01, min(0.99, 1.0 - ((_U_N0 - 2.0 * delta_AD_u) / 100.0)))
        _bg_dir  = "positive BG ↑" if delta_AD_u > 0 else "negative BG ↓"
        st.caption(
            f"AD shock: Δ = {delta_AD_u:+.1f} pp  →  "
            f"e = {_e_ad_sb*100:.1f}%  ({_bg_dir}  vs e*₀ = {_E_STAR0*100:.1f}%)"
        )
    mu_markup = st.slider(
        "Firm markup μ", 0.1, 0.8, 0.3, 0.05,
        key=f"mu_{_v}",
        help=(
            "Firm's price markup over costs. "
            "PS wage = 1/(1+μ). "
            "Higher μ → lower PS wage → lower e* → higher u_n."
        ),
    )
    delta_oil = st.slider(
        "Oil price shock (% change)", -0.20, 0.20, 0.0, 0.02,
        key=f"oil_{_v}",
        help=(
            "Oil price change as a fraction of costs (e.g. 0.10 = +10%). "
            "Positive: oil price rise → raises effective markup (μ_eff = μ + Δoil) "
            "→ PS curve shifts DOWN → positive BG at e*₀ → stagflation. "
            "Negative: oil price fall → PS shifts UP → disinflationary."
        ),
    )

    # Effective markup including oil shock
    _mu_eff    = mu_markup + delta_oil
    _w_ps_new  = 1.0 / (1.0 + _mu_eff)
    _e_star_new = float(max(0.01, min(0.99, (_w_ps_new - b_ws) / _GAMMA)))
    _u_n_new   = (1.0 - _e_star_new) * 100.0
    _delta_b   = b_ws - _B0
    _delta_mu  = (mu_markup - _MU0) + delta_oil
    _has_shock_sb = abs(_delta_b) > 0.001 or abs(_delta_mu) > 0.001
    if not _has_shock_sb:
        st.caption(
            f"Initial equilibrium (b={_B0:.2f}, μ={_MU0:.2f}):  "
            f"e*₀ = {_E_STAR0*100:.1f}%  →  uₙ₀ = {_U_N0:.1f}%  |  No shock"
        )
    else:
        _shock_str = "  |  "
        if abs(_delta_b) > 0.001:
            _shock_str += f"Δb = {_delta_b:+.2f}  "
        if abs(mu_markup - _MU0) > 0.001:
            _shock_str += f"Δμ = {mu_markup - _MU0:+.2f}  "
        if abs(delta_oil) > 0.001:
            _shock_str += f"Δoil = {delta_oil:+.2f}"
        st.caption(
            f"Initial: e*₀ = {_E_STAR0*100:.1f}%  uₙ₀ = {_U_N0:.1f}%{_shock_str}\n"
            f"New eq.: e*₁ = {_e_star_new*100:.1f}%  uₙ₁ = {_u_n_new:.1f}%"
        )

    # ── Phillips Curve ──────────────────────────────────────────────────────
    st.markdown("### 📈 Phillips Curve")
    alpha = st.slider(
        "Slope α", 0.1, 1.0, 0.1, 0.05,
        key=f"alpha_{_v}",
        help=(
            "Steepness of the SRPC. "
            "α = 1: 1% Bargaining Gap → 1 pp inflation above π^e. "
            "Lower α → flatter SRPC → slower inflation response."
        ),
    )

    # ── Central Bank ────────────────────────────────────────────────────────
    st.markdown("### 🏦 Central Bank")
    pi_star = st.slider(
        "Inflation target π* (%)", 0.0, 8.0, 2.0, 0.5,
        key=f"pistar_{_v}",
        help="The CB's announced inflation goal. Long-run equilibrium: (u_n, π*).",
    )
    phi = st.slider(
        "Policy intensity φ", 0.0, 8.0, 0.0, 0.25,
        key=f"phi_{_v}",
        help=(
            "CB reaction strength: u_t = u_n + φ·(π^e_t − π*). "
            "φ = 0 (default): fully accommodating — inflation spirals upward. "
            "Raise φ to see CB tighten unemployment toward the new u_n. "
            "Stability requires α·γ·φ/w_ps < 1."
        ),
    )
    _stab = alpha * _GAMMA * phi / _w_ps_new
    if _stab >= 1.0:
        st.warning(f"α·γ·φ/w_ps = {_stab:.2f} ≥ 1 — dynamics will oscillate.")

    # ── Expectations ────────────────────────────────────────────────────────
    st.markdown("### 🧠 Expectations")
    exp_type = st.selectbox(
        "Expectations formation",
        ["Adaptive", "Rational"],
        key=f"exp_{_v}",
        help=(
            "Adaptive (λ=1): π^e_t = π_{t−1}. Gradual adjustment, costly disinflation. "
            "Rational: π^e_t = π* immediately. Costless — illustrates the Lucas Critique."
        ),
    )
    pi_e_init = pi_star

    st.divider()
    if st.button("📖 How to Run", type="secondary", use_container_width=True,
                 help="Return to the introductory guide page."):
        st.session_state["intro_complete"] = False
        st.session_state["anim_running"]   = False
        st.rerun()
    if st.button("↺ Reset params", type="primary", use_container_width=True,
                 help="Reset all parameters to their default values."):
        st.session_state["param_ver"] += 1
        st.session_state["anim_frame"] = 0
        st.session_state["anim_running"] = False
        st.session_state["last_param_hash"] = ""
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 8. Run full simulation (always T_MAX+1 = 11 rows)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _run(alpha, pi_star, phi, n_periods, expectations,
         delta_b, delta_mu, delta_AD_u, gamma, b0, mu0):
    """Fixed constants (gamma, b0, mu0) are in the key so cache invalidates on code changes."""
    p = ModelParams(
        alpha=alpha, pi_star=pi_star, pi_e_init=pi_star,
        lambda_adapt=_LAMBDA, phi=phi,
        n_periods=n_periods, expectations=expectations,
        b=b0, gamma=gamma, mu=mu0, beta=_BETA,
        delta_b=delta_b, delta_mu=delta_mu, delta_AD_u=delta_AD_u,
    )
    return pd.DataFrame(PhillipsCurve(p).simulate())

_delta_b_run  = b_ws - _B0
_delta_mu_run = (mu_markup - _MU0) + delta_oil

df_full = _run(
    alpha, pi_star, phi, _T_MAX + 1, exp_type.lower(),
    _delta_b_run, _delta_mu_run, delta_AD_u,
    _GAMMA, _B0, _MU0,
)

# Rebuild model object fresh (not cached)
_params = ModelParams(
    alpha=alpha, pi_star=pi_star, pi_e_init=pi_star,
    lambda_adapt=_LAMBDA, phi=phi,
    n_periods=_T_MAX + 1, expectations=exp_type.lower(),
    b=_B0, gamma=_GAMMA, mu=_MU0, beta=_BETA,
    delta_b=_delta_b_run, delta_mu=_delta_mu_run, delta_AD_u=delta_AD_u,
)
_model = PhillipsCurve(_params)

# Pre-compute equilibrium values
u_n_val      = float(_model.p.u_n_derived)
u_n_post_val = float(_model.p.u_n_post)
e_star_val   = float(_model.p.e_star)
e_star_post  = float(_model.p.e_star_post)
has_shock    = abs(_delta_b_run) > 0.001 or abs(_delta_mu_run) > 0.001

# ─────────────────────────────────────────────────────────────────────────────
# 9. Determine T_max: convergence period or T_MAX
# ─────────────────────────────────────────────────────────────────────────────
def _find_t_max(df_f: pd.DataFrame, u_n_post: float, phi_val: float) -> int:
    """Stop animation when u converges within 0.2 pp of u_n_post (CB active only)."""
    if phi_val < 0.01:
        return _T_MAX
    tol = 0.2
    for t in range(1, _T_MAX + 1):
        if abs(float(df_f["u"].iloc[t]) - u_n_post) < tol:
            return t
    return _T_MAX

_anim_t_max = _find_t_max(df_full, u_n_post_val, phi)

# ─────────────────────────────────────────────────────────────────────────────
# 10. Detect parameter changes → auto-animate (not on first load)
# ─────────────────────────────────────────────────────────────────────────────
_param_hash = hashlib.md5(
    f"{b_ws:.4f}{mu_markup:.4f}{delta_oil:.4f}{delta_AD_u:.2f}"
    f"{alpha:.4f}{pi_star:.2f}{phi:.4f}{exp_type}".encode()
).hexdigest()[:8]

_is_first_load = (st.session_state["last_param_hash"] == "")
if _param_hash != st.session_state["last_param_hash"]:
    st.session_state["last_param_hash"] = _param_hash
    st.session_state["anim_frame"]  = 0
    st.session_state["anim_t_max"]  = _anim_t_max
    if not _is_first_load:
        st.session_state["anim_running"] = True

# Clamp frame to valid range
_frame = min(int(st.session_state["anim_frame"]), _anim_t_max)
st.session_state["anim_frame"] = _frame

# Slice data to current frame
df = df_full.iloc[:_frame + 1].copy()

_e_ax_lo = 0.2
_e_ax_hi = 1.0

# ─────────────────────────────────────────────────────────────────────────────
# 11. Tabs
# ─────────────────────────────────────────────────────────────────────────────
tab_sim, tab_theory, tab_quiz = st.tabs(["📊 Simulation", "📖 Theory", "📝 Quiz"])

# =============================================================================
# TAB 1 — Simulation
# =============================================================================
with tab_sim:

    # ── Animation controls ────────────────────────────────────────────────────
    _ac1, _ac2, _ac3, _ac4 = st.columns([1, 1, 1, 5])
    with _ac1:
        if st.session_state["anim_running"]:
            if st.button("⏸ Pause", type="secondary", use_container_width=True):
                st.session_state["anim_running"] = False
                st.rerun()
        else:
            if st.button("▶ Play", type="primary", use_container_width=True):
                st.session_state["anim_frame"]  = 0
                st.session_state["anim_running"] = True
                st.rerun()
    with _ac2:
        if st.button("⏮ Reset", type="secondary", use_container_width=True):
            st.session_state["anim_frame"]   = 0
            st.session_state["anim_running"] = False
            st.rerun()
    with _ac3:
        if st.button("⏭ Final", type="secondary", use_container_width=True):
            st.session_state["anim_frame"]   = _anim_t_max
            st.session_state["anim_running"] = False
            st.rerun()
    with _ac4:
        _converged = (
            phi > 0.01 and _frame > 0
            and abs(float(df_full["u"].iloc[_frame]) - u_n_post_val) < 0.2
        )
        _status = (
            "▶ animating…" if st.session_state["anim_running"]
            else ("✓ converged" if _converged else "⏸ paused")
        )
        st.markdown(
            f'<div class="period-badge">'
            f'Period &nbsp; t = {_frame} / {_anim_t_max} &nbsp;·&nbsp; {_status}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    with st.expander("💡 How to use this simulation", expanded=False):
        st.markdown(
            "**Shift any slider and the simulation animates automatically.**\n"
            "- With φ = 0 (no CB response): animation runs for 10 periods.\n"
            "- With φ > 0 (CB active): animation stops when unemployment converges.\n\n"
            "**Scenarios to try:**\n\n"
            "*1 — Markup shock (stagflation):* Increase μ above 0.30. "
            "The PS line shifts DOWN. BG > 0 opens at e*₀. Inflation spirals up.\n\n"
            "*2 — AD boom (movement along SRPC):* Set AD demand shock to +6. "
            "Employment rises above e*₀. Inflation rises in period 1. "
            "From period 2, the SRPC shifts upward as expectations adapt.\n\n"
            "*3 — CB response:* Raise φ. Unemployment rises toward the new u_n. "
            "Animation stops at convergence.\n\n"
            "*4 — Lucas Critique:* With any shock active, switch Expectations to Rational. "
            "Disinflation becomes costless — the SRPC collapses in one step.\n\n"
            "*5 — Oil price shock:* Set Oil price shock to +15%. Same stagflation as markup. "
            "A negative value (−10%) simulates a favourable oil supply shock.\n\n"
            "*6 — Bargaining power shock:* Raise WS intercept b above 0.30. "
            "WS shifts up → new lower e*₁ → positive BG at old e*₀ → stagflation."
        )

    st.markdown("---")

    # ── Key metrics ────────────────────────────────────────────────────────────
    _m1, _m2, _m3 = st.columns(3)
    if has_shock:
        _m1.metric(
            "Natural rate uₙ₀ → uₙ₁",
            f"{u_n_post_val:.1f}%",
            delta=f"{u_n_post_val - u_n_val:+.1f}pp",
        )
    else:
        _m1.metric("Natural rate uₙ (%)", f"{u_n_val:.1f}%")
    _pi_current = float(df["pi"].iloc[-1])
    _u_current  = float(df["u"].iloc[-1])
    _m2.metric(
        f"Inflation at t={_frame}", f"{_pi_current:.2f}%",
        delta=f"{_pi_current - pi_star:+.2f}pp vs π*",
    )
    _m3.metric(
        f"Unemployment at t={_frame}", f"{_u_current:.1f}%",
        delta=f"{_u_current - (u_n_post_val if has_shock else u_n_val):+.1f}pp vs uₙ",
    )

    # ── Current period status box ───────────────────────────────────────────
    if _frame > 0:
        _bg_cur = float(df["bg"].iloc[-1]) * 100.0
        _pie_cur = float(df["pi_e"].iloc[-1])
        _e_cur   = float(df["e"].iloc[-1])
        _bg_label = (
            "positive ↑ (inflationary)" if _bg_cur > 0.01
            else "negative ↓ (disinflationary)" if _bg_cur < -0.01
            else "zero (equilibrium)"
        )
        st.markdown(
            f'<div class="status-box">'
            f'<b>t = {_frame}:</b> &nbsp; '
            f'e = {_e_cur*100:.1f}% &nbsp;·&nbsp; '
            f'u = {_u_current:.1f}% &nbsp;·&nbsp; '
            f'BG = {_bg_cur:+.2f}% ({_bg_label}) &nbsp;·&nbsp; '
            f'π = {_pi_current:.2f}% &nbsp;·&nbsp; '
            f'π<sup>e</sup> = {_pie_cur:.2f}%'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ═════════════════════════════════════════════════════════════════════════
    # WS/PS Labour Market Diagram
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown(
        '<h3 class="section-h">WS/PS Labour Market Diagram</h3>',
        unsafe_allow_html=True,
    )
    st.caption(
        "WS and PS curves define the labour market equilibrium e* and natural rate u_n. "
        "The coloured dot (●) tracks the economy's employment position each period. "
        "The orange/purple bar is the Bargaining Gap — the engine of inflation dynamics."
    )

    e_range_ws        = np.linspace(0.0, 1.0, 200)
    ws_curve_pre      = _model.ws_curve(e_range_ws)
    ps_pre            = _model.ps_level()
    ws_curve_post_arr = _model.ws_curve_post(e_range_ws)
    ps_post           = _model.ps_level_post()

    _eq_valid   = 0.02 < e_star_val < 0.98
    _bg_at_e0   = _model.bargaining_gap_post(e_star_val) if has_shock else 0.0
    _bg_pct     = _bg_at_e0 * 100.0

    _all_ws = np.concatenate([ws_curve_pre, ws_curve_post_arr])
    _all_ps = [ps_pre, ps_post]
    y_lo = min(float(_all_ws.min()), min(_all_ps)) - 0.05
    y_hi = max(float(_all_ws.max()), max(_all_ps)) + 0.14

    fig_ws = go.Figure()

    if _eq_valid:
        fig_ws.add_vrect(
            x0=e_star_val, x1=1.0,
            fillcolor="rgba(239,68,68,0.08)", line_width=0,
        )
        fig_ws.add_annotation(
            x=(e_star_val + 1.0) / 2, y=y_hi * 0.96,
            text=f"Unemployment<br>u<sub>n</sub>₀ = {u_n_val:.1f}%",
            showarrow=False, font=dict(color="#ef4444", size=11), align="center",
        )

    if has_shock:
        fig_ws.add_trace(go.Scatter(
            x=e_range_ws, y=ws_curve_pre,
            mode="lines", line=dict(color="#94a3b8", width=1.8, dash="dash"),
            name="WS₀ (initial)",
            hovertemplate="e=%{x:.3f} | WS₀=%{y:.3f}<extra></extra>",
        ))
        fig_ws.add_trace(go.Scatter(
            x=[0.0, 1.0], y=[ps_pre, ps_pre],
            mode="lines", line=dict(color="#94a3b8", width=1.8, dash="dash"),
            name=f"PS₀ = {ps_pre:.3f}  (initial)",
            hovertemplate=f"PS₀ = {ps_pre:.3f}<extra></extra>",
        ))

    _ws_label = "WS₁ (new)" if has_shock else "Wage-Setting (WS)"
    _ps_label = f"PS₁ = {ps_post:.3f}  (new)" if has_shock else "Price-Setting (PS)"
    fig_ws.add_trace(go.Scatter(
        x=e_range_ws, y=ws_curve_post_arr,
        mode="lines", line=dict(color="#4338ca", width=2.5),
        name=_ws_label,
        hovertemplate="e=%{x:.3f} | WS=%{y:.3f}<extra></extra>",
    ))
    fig_ws.add_trace(go.Scatter(
        x=[0.0, 1.0], y=[ps_post, ps_post],
        mode="lines", line=dict(color="#16a34a", width=2.5),
        name=_ps_label,
        hovertemplate=f"PS = {ps_post:.3f}<extra></extra>",
    ))

    if _eq_valid:
        fig_ws.add_shape(type="line",
            x0=e_star_val, x1=e_star_val, y0=y_lo, y1=ps_pre,
            line=dict(color="#ef4444", width=1.5, dash="dot"))
        fig_ws.add_shape(type="line",
            x0=0.0, x1=e_star_val, y0=ps_pre, y1=ps_pre,
            line=dict(color="#ef4444", width=1.5, dash="dot"))
        fig_ws.add_trace(go.Scatter(
            x=[e_star_val], y=[ps_pre],
            mode="markers",
            marker=dict(size=12, color="#ef4444", symbol="circle",
                        line=dict(color="white", width=2)),
            name="e*₀ equilibrium (BG=0 at t=0)",
            hovertemplate=f"e*₀={e_star_val*100:.1f}% | w*₀={ps_pre:.3f}<extra></extra>",
        ))
        fig_ws.add_annotation(x=e_star_val, y=y_lo,
            text=f"<b>e*₀={e_star_val*100:.1f}%</b>",
            showarrow=False, yanchor="top", yshift=-4,
            font=dict(color="#ef4444", size=12))
        fig_ws.add_annotation(x=0.0, y=ps_pre,
            text=f"<b>w*₀={ps_pre:.3f}</b>",
            showarrow=False, xanchor="right", xshift=-6,
            font=dict(color="#ef4444", size=12))

    _eq1_valid = 0.02 < e_star_post < 0.98
    if has_shock and _eq1_valid:
        fig_ws.add_shape(type="line",
            x0=e_star_post, x1=e_star_post, y0=y_lo, y1=ps_post,
            line=dict(color="#0ea5e9", width=1.5, dash="dot"))
        if abs(_delta_mu_run) > 0.001:
            fig_ws.add_shape(type="line",
                x0=0.0, x1=e_star_post, y0=ps_post, y1=ps_post,
                line=dict(color="#0ea5e9", width=1.2, dash="dot"))
            fig_ws.add_annotation(x=0.0, y=ps_post,
                text=f"<b>w*₁={ps_post:.3f}</b>",
                showarrow=False, xanchor="right", xshift=-6,
                font=dict(color="#0ea5e9", size=12))
        fig_ws.add_trace(go.Scatter(
            x=[e_star_post], y=[ps_post],
            mode="markers",
            marker=dict(size=12, color="#0ea5e9", symbol="diamond",
                        line=dict(color="white", width=2)),
            name=f"e*₁ new equilibrium  (uₙ₁={u_n_post_val:.1f}%)",
            hovertemplate=f"e*₁={e_star_post*100:.1f}% | w*₁={ps_post:.3f}<extra></extra>",
        ))
        _e1_label_yshift = -22 if abs(e_star_post - e_star_val) < 0.04 else -4
        fig_ws.add_annotation(x=e_star_post, y=y_lo,
            text=f"<b>e*₁={e_star_post*100:.1f}%</b>",
            showarrow=abs(e_star_post - e_star_val) < 0.04,
            arrowhead=2, arrowcolor="#0ea5e9", ax=0, ay=16,
            yanchor="top", yshift=_e1_label_yshift,
            font=dict(color="#0ea5e9", size=12))

    # AD shock employment point
    _has_ad = abs(delta_AD_u) > 0.01
    if _has_ad and _eq_valid:
        _e_ad    = max(0.01, min(0.99, 1.0 - ((_U_N0 - 2.0 * delta_AD_u) / 100.0)))
        _w_ps_ad = ps_post if has_shock else ps_pre
        _w_ws_ad = float(_model.ws_curve_post(np.array([_e_ad]))[0]) if has_shock \
                   else float(_model.ws_curve(np.array([_e_ad]))[0])
        _bg_ad_pct = (_w_ws_ad - _w_ps_ad) / _w_ps_ad * 100.0
        _ad_col = "#16a34a"
        fig_ws.add_shape(type="line",
            x0=_e_ad, x1=_e_ad, y0=y_lo, y1=_w_ps_ad,
            line=dict(color=_ad_col, width=1.5, dash="dot"))
        fig_ws.add_trace(go.Scatter(
            x=[_e_ad], y=[_w_ps_ad],
            mode="markers",
            marker=dict(size=11, color=_ad_col, symbol="circle",
                        line=dict(color="white", width=2)),
            name=f"AD shock employment  (e={_e_ad*100:.1f}%)",
            hovertemplate=f"AD: e={_e_ad*100:.1f}% | w_PS={_w_ps_ad:.3f}<extra></extra>",
        ))
        fig_ws.add_annotation(x=_e_ad, y=y_lo,
            text=f"<b>e_AD={_e_ad*100:.1f}%</b>",
            showarrow=False, yanchor="top", yshift=-4,
            font=dict(color=_ad_col, size=12))
        if abs(_bg_ad_pct) > 0.01:
            _gap_bot_ad = min(_w_ws_ad, _w_ps_ad)
            _gap_top_ad = max(_w_ws_ad, _w_ps_ad)
            _gap_dir_ad = "↑ BG > 0" if _bg_ad_pct > 0 else "↓ BG < 0"
            _gap_col_ad = "#f97316" if _bg_ad_pct > 0 else "#8b5cf6"
            fig_ws.add_shape(type="line",
                x0=_e_ad, x1=_e_ad, y0=_gap_bot_ad, y1=_gap_top_ad,
                line=dict(color=_gap_col_ad, width=3))
            fig_ws.add_annotation(
                x=_e_ad, y=(_gap_bot_ad + _gap_top_ad) / 2,
                text=f"<b>{_gap_dir_ad}<br>BG={_bg_ad_pct:+.1f}%<br>at e_AD</b>",
                showarrow=True, arrowhead=2, arrowcolor=_gap_col_ad,
                ax=-40, ay=0, xanchor="right",
                font=dict(color=_gap_col_ad, size=11),
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor=_gap_col_ad, borderwidth=1,
            )

    # BG arrow at e*₀ under new curves (structural shock)
    if has_shock and _eq_valid and abs(_bg_pct) > 0.01:
        _ws_new_at_e0 = float(_model.ws_curve_post(np.array([e_star_val]))[0])
        _gap_bot = min(_ws_new_at_e0, ps_post)
        _gap_top = max(_ws_new_at_e0, ps_post)
        _gap_dir = "↑ BG > 0" if _bg_pct > 0 else "↓ BG < 0"
        _gap_col = "#f97316" if _bg_pct > 0 else "#8b5cf6"
        fig_ws.add_shape(type="line",
            x0=e_star_val, x1=e_star_val, y0=_gap_bot, y1=_gap_top,
            line=dict(color=_gap_col, width=3))
        fig_ws.add_annotation(
            x=e_star_val, y=(_gap_bot + _gap_top) / 2,
            text=f"<b>{_gap_dir}<br>BG={_bg_pct:+.1f}%<br>at e*₀</b>",
            showarrow=True, arrowhead=2, arrowcolor=_gap_col,
            ax=40, ay=0, xanchor="left",
            font=dict(color=_gap_col, size=11),
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor=_gap_col, borderwidth=1,
        )

    # ── Animated economy dot — shows current period's employment ─────────────
    if _frame > 0:
        _e_now   = float(df["e"].iloc[-1])
        _w_ws_now = float(df["w_ws"].iloc[-1])
        _w_ps_now = float(df["w_ps"].iloc[-1])
        _bg_now  = float(df["bg"].iloc[-1])
        _dot_col = "#f97316" if _bg_now > 0.001 else "#8b5cf6" if _bg_now < -0.001 else "#22c55e"
        # BG bar at current employment
        if abs(_bg_now) > 0.0001:
            fig_ws.add_shape(type="line",
                x0=_e_now, x1=_e_now,
                y0=min(_w_ws_now, _w_ps_now), y1=max(_w_ws_now, _w_ps_now),
                line=dict(color=_dot_col, width=4))
        # Current employment dot
        fig_ws.add_trace(go.Scatter(
            x=[_e_now], y=[_w_ps_now],
            mode="markers+text",
            marker=dict(size=16, color=_dot_col, symbol="circle",
                        line=dict(color="white", width=2.5)),
            text=[f"t={_frame}"],
            textposition="top right",
            textfont=dict(size=12, color=_dot_col),
            name=f"Economy at t={_frame}  (e={_e_now*100:.1f}%)",
            hovertemplate=(
                f"t={_frame} | e={_e_now*100:.1f}% "
                f"| BG={_bg_now*100:+.2f}%<extra></extra>"
            ),
        ))

    if not _eq_valid:
        fig_ws.add_annotation(
            x=0.5, y=(y_lo + y_hi) / 2,
            text="⚠️ WS and PS do not intersect<br>Bargaining Gap not defined.<br>Adjust b or μ.",
            showarrow=False, align="center",
            font=dict(color="#dc2626", size=13),
            bgcolor="rgba(254,242,242,0.9)",
            bordercolor="#dc2626", borderwidth=1,
        )

    fig_ws.add_annotation(x=1.0, y=y_lo, text="<b>LF</b>",
        showarrow=False, yanchor="top", yshift=-4,
        font=dict(color="#64748b", size=12))

    fig_ws.update_layout(
        template="plotly_white", height=420,
        font=dict(family="Georgia, serif", size=13, color="#1e293b"),
        xaxis=dict(
            title=dict(text="Employment Rate  (e)", font=dict(size=14, color="#1e293b")),
            tickfont=dict(size=12, color="#1e293b"),
            range=[_e_ax_lo, _e_ax_hi], tickformat=".0%",
        ),
        yaxis=dict(
            title=dict(text="Real Wage  (w)", font=dict(size=14, color="#1e293b")),
            tickfont=dict(size=12, color="#1e293b"),
            range=[y_lo, y_hi],
        ),
        legend=dict(
            x=0.02, y=0.98, xanchor="left", yanchor="top",
            bgcolor="rgba(255,255,255,0.92)", bordercolor="#e2e8f0",
            borderwidth=1, font=dict(size=11, color="#1e293b"),
        ),
        margin=dict(l=80, r=60, t=40, b=70),
        paper_bgcolor="white", plot_bgcolor="#fafafa",
    )
    st.plotly_chart(fig_ws, use_container_width=True)

    if not _eq_valid:
        st.warning(
            "Labour market has no equilibrium — "
            "Bargaining Gap cannot be computed. Adjust b or μ sliders."
        )

    # ═════════════════════════════════════════════════════════════════════════
    # Phillips Curve Diagram
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown(
        '<h3 class="section-h">Phillips Curve: Inflation vs. Employment</h3>',
        unsafe_allow_html=True,
    )
    st.caption(
        "The SRPC shifts upward each period as inflation expectations adjust. "
        "The path traces the economy through (e, π) space. "
        "The amber dot (●) marks the current period's position."
    )

    e_range_ph = np.linspace(0.0, 1.0, 400)
    _pi_lo = min(0.0, float(df_full["pi"].min()) - 1.5, float(df_full["pi_e"].min()) - 1.5)
    _pi_hi = max(float(pi_star) + 2.0, float(df_full["pi"].max()) + 2.0,
                 float(df_full["pi_e"].max()) + 2.0)

    # SRPC family — accumulate curves up to current frame
    _srpc_entries: list[dict] = []
    _seen_keys: set = set()
    for _t in range(_frame + 1):
        _pie_t     = round(float(df_full["pi_e"].iloc[_t]), 6)
        _post_flag = has_shock and _t > 0
        _key       = (_pie_t, _post_flag)
        if _key not in _seen_keys:
            _seen_keys.add(_key)
            _srpc_entries.append({
                "t":     _t,
                "label": f"SRPC (t={_t}, πᵉ={_pie_t:.2f}%)",
                "pi_e":  _pie_t,
                "post":  _post_flag,
            })

    _bg1 = _bg_at_e0 if has_shock else 0.0
    _nc  = max(len(_srpc_entries) - 1, 1)

    def _lerp_ph(frac: float) -> str:
        if _bg1 >= 0:
            r = int(148 + frac * (249 - 148))
            g = int(163 + frac * (115 - 163))
            b_c = int(184 + frac * (22  - 184))
        else:
            r = int(148 + frac * (67  - 148))
            g = int(163 + frac * (56  - 163))
            b_c = int(184 + frac * (202 - 184))
        return f"rgb({r},{g},{b_c})"

    fig_ph = go.Figure()

    for _i, _s in enumerate(_srpc_entries):
        _frac  = _i / _nc
        _color = _lerp_ph(_frac)
        _dash  = "dash" if _i == 0 else ("solid" if _i == len(_srpc_entries) - 1 else "dot")
        _width = 2.2 if (_i == 0 or _i == len(_srpc_entries) - 1) else 1.4
        _pi_s  = _model.srpc_in_e(_s["pi_e"], e_range_ph, post=_s["post"])
        _mask  = (_pi_s >= _pi_lo) & (_pi_s <= _pi_hi)
        fig_ph.add_trace(go.Scatter(
            x=e_range_ph[_mask], y=_pi_s[_mask],
            mode="lines",
            line=dict(color=_color, width=_width, dash=_dash),
            name=_s["label"],
            hovertemplate=f"{_s['label']} | e=%{{x:.3f}} | π=%{{y:.2f}}%<extra></extra>",
        ))

    fig_ph.add_vline(
        x=e_star_val,
        line=dict(color="#64748b", width=1.8, dash="dash"),
        annotation_text=f"LRPC₀ (e*₀={e_star_val*100:.1f}%)",
        annotation_position="top right",
        annotation_font=dict(color="#64748b", size=11),
    )
    if has_shock and abs(e_star_post - e_star_val) > 0.005:
        fig_ph.add_vline(
            x=e_star_post,
            line=dict(color="#94a3b8", width=1.5, dash="dot"),
            annotation_text=f"LRPC₁ (e*₁={e_star_post*100:.1f}%)",
            annotation_position="top left",
            annotation_font=dict(color="#94a3b8", size=11),
        )

    fig_ph.add_hline(
        y=pi_star,
        line=dict(color="#22c55e", width=1.5, dash="dash"),
        annotation_text=f"π* = {pi_star:.1f}%",
        annotation_position="right",
        annotation_font=dict(color="#22c55e", size=12),
    )

    # Economy path (accumulated to current frame)
    _t_pos = ["top right" if i % 2 == 0 else "bottom left" for i in range(len(df))]
    fig_ph.add_trace(go.Scatter(
        x=df["e"], y=df["pi"],
        mode="lines+markers+text",
        line=dict(color="#334155", width=2),
        marker=dict(size=8, color="#334155", line=dict(color="white", width=1.5)),
        text=[f"t={t}" for t in df["t"]],
        textposition=_t_pos,
        textfont=dict(size=11, color="#334155"),
        name="Path of Economy",
        hovertemplate="t=%{customdata} | e=%{x:.3f} | π=%{y:.2f}%<extra></extra>",
        customdata=df["t"],
    ))

    fig_ph.add_trace(go.Scatter(
        x=[e_star_val], y=[pi_star],
        mode="markers",
        marker=dict(size=18, color="#16a34a", symbol="star",
                    line=dict(width=2, color="white")),
        name=f"Initial Equilibrium  (e*₀={e_star_val*100:.1f}%, π*={pi_star:.1f}%)",
        hovertemplate=f"Initial Eq. | e*₀={e_star_val*100:.1f}% | π*={pi_star:.2f}%<extra></extra>",
    ))

    # Animated current-period dot (amber)
    if _frame > 0:
        _e_now_ph = float(df["e"].iloc[-1])
        _pi_now   = float(df["pi"].iloc[-1])
        fig_ph.add_trace(go.Scatter(
            x=[_e_now_ph], y=[_pi_now],
            mode="markers",
            marker=dict(size=14, color="#f59e0b", symbol="circle",
                        line=dict(color="white", width=2.5)),
            name=f"Current position (t={_frame})",
            hovertemplate=f"t={_frame} | e={_e_now_ph*100:.1f}% | π={_pi_now:.2f}%<extra></extra>",
        ))

    fig_ph.update_layout(
        template="plotly_white", height=520,
        font=dict(family="Georgia, serif", size=13, color="#1e293b"),
        xaxis=dict(
            title=dict(text="Employment Rate  (e)", font=dict(size=14, color="#1e293b")),
            tickfont=dict(size=12, color="#1e293b"),
            range=[_e_ax_lo, _e_ax_hi], tickformat=".0%",
        ),
        yaxis=dict(
            title=dict(text="Inflation Rate  π (%)", font=dict(size=14, color="#1e293b")),
            tickfont=dict(size=12, color="#1e293b"),
            range=[_pi_lo, _pi_hi], ticksuffix="%",
        ),
        legend=dict(
            orientation="h", x=0.5, y=-0.12,
            xanchor="center", yanchor="top",
            bgcolor="rgba(255,255,255,0.92)", bordercolor="#e2e8f0",
            borderwidth=1, font=dict(size=11, color="#1e293b"),
        ),
        margin=dict(l=60, r=80, t=40, b=110),
        paper_bgcolor="white", plot_bgcolor="#fafafa",
    )
    st.plotly_chart(fig_ph, use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # Time Series
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown(
        '<h3 class="section-h">Time Series: Inflation &amp; Unemployment</h3>',
        unsafe_allow_html=True,
    )

    fig_ts = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=(
            "Inflation (%) — actual π and expectations π<sup>e</sup>",
            "Unemployment (%) — actual u vs. natural rate u_n",
        ),
        vertical_spacing=0.13,
    )

    fig_ts.add_trace(go.Scatter(
        x=df["t"], y=df["pi_e"],
        mode="lines+markers",
        line=dict(color="#818cf8", width=2.5, dash="dot"),
        marker=dict(size=6),
        name="π\u1d49 Expectations",
    ), row=1, col=1)

    fig_ts.add_trace(go.Scatter(
        x=df["t"], y=df["pi"],
        mode="lines+markers",
        line=dict(color="#f97316", width=2.5),
        marker=dict(size=6),
        name="Actual π",
    ), row=1, col=1)

    fig_ts.add_hline(
        y=pi_star, row=1, col=1,
        line=dict(color="#22c55e", width=1.5, dash="dash"),
        annotation_text=f"π* = {pi_star:.1f}%",
        annotation_position="right",
        annotation_font=dict(color="#22c55e", size=12),
    )

    fig_ts.add_trace(go.Scatter(
        x=df["t"], y=df["u"],
        mode="lines+markers",
        line=dict(color="#475569", width=2.5),
        marker=dict(size=6),
        name="Unemployment u",
    ), row=2, col=1)

    fig_ts.add_hline(
        y=u_n_val, row=2, col=1,
        line=dict(color="#ef4444", width=1.5, dash="dot"),
        annotation_text=f"uₙ₀ = {u_n_val:.1f}%",
        annotation_position="top right",
        annotation_font=dict(color="#ef4444", size=11),
    )

    if has_shock and abs(u_n_post_val - u_n_val) > 0.05:
        _u_n_series = np.where(df["t"].values == 0, u_n_val, u_n_post_val)
        fig_ts.add_trace(go.Scatter(
            x=df["t"], y=_u_n_series,
            mode="lines",
            line=dict(color="#dc2626", width=2.0, dash="dash", shape="hv"),
            name=f"uₙ₁ (new, {u_n_post_val:.1f}%)",
            hovertemplate="t=%{x} | uₙ₁=%{y:.1f}%<extra></extra>",
        ), row=2, col=1)

    # Fixed axis ranges (from df_full) — prevents jarring resize during animation
    _ts_x_hi  = _anim_t_max + 0.3
    _ts_pi_lo = min(0.0, float(df_full["pi"].min()) - 0.5, float(df_full["pi_e"].min()) - 0.5)
    _ts_pi_hi = max(float(pi_star) + 2.0, float(df_full["pi"].max()) + 1.0,
                    float(df_full["pi_e"].max()) + 1.0)
    _ts_u_lo  = max(0.0, min(float(df_full["u"].min()), u_n_val, u_n_post_val) - 1.0)
    _ts_u_hi  = max(float(df_full["u"].max()), u_n_val, u_n_post_val) + 2.0

    fig_ts.update_layout(
        template="plotly_white", height=500,
        font=dict(family="Georgia, serif", size=13, color="#1e293b"),
        legend=dict(
            orientation="h", x=0.5, y=-0.12,
            xanchor="center", yanchor="top",
            bgcolor="rgba(255,255,255,0.92)", bordercolor="#e2e8f0",
            borderwidth=1, font=dict(size=12, color="#1e293b"),
        ),
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(r=90, b=80),
    )
    fig_ts.update_yaxes(
        range=[_ts_pi_lo, _ts_pi_hi], ticksuffix="%",
        title_font=dict(size=14, color="#1e293b"),
        tickfont=dict(size=12, color="#1e293b"), row=1, col=1,
    )
    fig_ts.update_yaxes(
        range=[_ts_u_lo, _ts_u_hi], ticksuffix="%",
        title_font=dict(size=14, color="#1e293b"),
        tickfont=dict(size=12, color="#1e293b"), row=2, col=1,
    )
    fig_ts.update_xaxes(
        title_text="Period t", row=2, col=1,
        title_font=dict(size=14, color="#1e293b"),
        tickfont=dict(size=12, color="#1e293b"),
        tickmode="linear", dtick=1,
        range=[-0.3, _ts_x_hi],
    )
    fig_ts.update_xaxes(
        tickfont=dict(size=12, color="#1e293b"),
        tickmode="linear", dtick=1,
        range=[-0.3, _ts_x_hi],
        row=1, col=1,
    )
    fig_ts.update_annotations(font=dict(size=13, color="#1e293b"))
    st.plotly_chart(fig_ts, use_container_width=True)

    with st.expander("🔢 Raw simulation data"):
        fmt_dict = {
            "u": "{:.3f}%", "pi": "{:.3f}%", "pi_e": "{:.3f}%",
            "e": "{:.4f}", "bg": "{:+.4f}", "w_ws": "{:.4f}", "w_ps": "{:.4f}",
        }
        st.dataframe(df.style.format(fmt_dict), use_container_width=True)

# =============================================================================
# TAB 2 — Theory
# =============================================================================
with tab_theory:
    st.markdown(
        '<h2 class="section-h">WS/PS Labour Market &amp; Phillips Curve: Theory</h2>',
        unsafe_allow_html=True,
    )

    st.markdown("### 1. WS/PS Labour Market & the Bargaining Gap")
    st.latex(r"w^{WS}(e) = b + \gamma \cdot e \qquad \text{(Wage-Setting — upward-sloping)}")
    st.latex(r"w^{PS} = \frac{1}{1+\mu} \qquad \text{(Price-Setting — flat)}")
    st.latex(r"e^* = \frac{w^{PS} - b}{\gamma} \;\Rightarrow\; u_n = (1 - e^*)\times 100")
    st.latex(
        r"\text{gap}_t = \frac{w^{WS}(e_t) - w^{PS}}{w^{PS}} "
        r"\quad \text{(Bargaining Gap — fraction of PS wage)}"
    )
    st.markdown(r"""
The BG measures by what **percentage** workers' wage demands exceed (or fall short of)
what firms can pay.  Evaluated at the **current employment** $e_t$ each period.

| Symbol | Meaning |
|--------|---------|
| $b$ | WS intercept — workers' outside option |
| $\gamma > 0$ | WS slope — sensitivity of bargained wage to employment |
| $\mu$ | Firm markup; $w^{PS} = 1/(1+\mu)$ flat |
| $e^*$ | Equilibrium employment (BG = 0) |
| $\text{gap}_t$ | BG fraction: positive when $e_t > e^*$ |

**Equilibrium:** When $e_t = e^*$, BG = 0 and $\pi_t = \pi_t^e$.
The CB's reaction function moves $u_t$ away from $u_n$ whenever $\pi_t^e \neq \pi^*$,
opening a non-zero BG that drives inflation above or below target.
    """)

    st.divider()

    st.markdown("### 2. Short-Run Phillips Curve (SRPC) — WS/PS formulation")
    st.latex(
        r"\pi_t \;=\; \pi_t^e \;+\; \alpha \cdot \text{scale} \cdot \text{gap}_t \times 100 "
        r"\;+\; \varepsilon_t"
    )
    st.latex(
        r"\text{scale} = \begin{cases} 1 & \text{if gap}_t \ge 0 "
        r"\text{ (positive BG — full pass-through)} \\ "
        r"\beta & \text{if gap}_t < 0 "
        r"\text{ (negative BG — dampened by downward wage rigidity)} \end{cases}"
    )
    st.markdown(r"""
The SRPC passes through $(u_n,\, \pi^e)$ and is **kinked at** $u_n$:
- Left of $u_n$ ($e > e^*$, positive BG): slope $= \alpha\gamma/w^{PS}$
- Right of $u_n$ ($e < e^*$, negative BG): slope $= \beta\alpha\gamma/w^{PS}$ (shallower)

This **asymmetric curvature** (β < 1) reflects downward nominal wage rigidity:
inflation accelerates faster in booms than it decelerates in recessions.

| Symbol | Meaning |
|--------|---------|
| $\alpha > 0$ | BG pass-through sensitivity |
| $\beta \in (0,1]$ | Wage-rigidity damping ($\beta=1$ → symmetric) |
| $\varepsilon_t$ | Supply shock (direct inflation hit) |
    """)

    st.divider()

    st.markdown("### 3. Expectations Formation")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Adaptive Expectations")
        st.latex(r"\pi_t^e = \pi_{t-1}^e + \lambda\!\left(\pi_{t-1} - \pi_{t-1}^e\right)")
        st.latex(r"\xrightarrow{\lambda=1}\; \pi_t^e = \pi_{t-1} \qquad \text{(standard adaptive case)}")
        st.markdown("""
Agents look **backward**: always expect this period's inflation = last period's actual.

- **Implication:** Disinflation is gradual and costly — SRPC shifts down slowly,
  requiring sustained $u > u_n$ and a positive sacrifice ratio.
        """)
    with col_b:
        st.markdown("#### Rational Expectations")
        st.latex(r"\pi_t^e = \pi^* \quad \text{(credible CB)}")
        st.markdown("""
Agents use **all available information**, including the policy rule.

- If the CB credibly commits to $\\pi^*$, agents set $\\pi^e = \\pi^*$ immediately.
- **Implication:** A credible announcement eliminates the sacrifice ratio.
        """)

    st.divider()

    st.markdown("### 4. Central Bank Reaction Function")
    st.latex(r"u_t = u_{n1} + \varphi \cdot \max\!\left(0,\; \pi_t^e - \pi^*\right)")
    st.markdown("""
The CB tightens (raising $u$ above the **post-shock** structural rate $u_{n1}$) whenever
expected inflation exceeds target:

- $\\varphi = 0$: Fully **accommodating** — inflation persists, no sacrifice ratio.
- Large $\\varphi$: **Aggressive** — rapid disinflation at the cost of a deeper recession.
- **Stability condition (WS/PS mode):** $\\alpha \\cdot \\gamma \\cdot \\varphi / w^{PS} < 1$.
    """)

    st.divider()

    st.markdown("### 5. Long-Run Phillips Curve (LRPC)")
    st.latex(r"\text{In LR equilibrium: } \pi_t = \pi_t^e \;\Rightarrow\; u_t = u_{n1}")
    st.markdown("""
The LRPC is a **vertical line at** $u = u_{n1}$ (the post-shock structural rate).

After a permanent WS or PS shift, $u_{n1} > u_{n0}$:
the LRPC shifts **right** — a permanent rise in structural unemployment.
There is no long-run inflation-unemployment trade-off.
    """)

    st.divider()

    st.markdown("### 6. The Lucas Critique")
    st.markdown("""
> *"Any change in policy will systematically alter the structure of econometric models."*
> — Robert E. Lucas Jr. (1976)

Applied to the Phillips Curve:
1. Policymakers observe a stable SRPC and exploit it.
2. Forward-looking agents **anticipate this** and raise $\\pi^e$, shifting the SRPC upward.
3. The original trade-off **vanishes** — the curve was never a stable structural relationship.
    """)

    st.divider()

    st.markdown("### 7. Sacrifice Ratio")
    st.latex(
        r"\text{Sacrifice Ratio} \;=\; "
        r"\frac{\displaystyle\sum_{t} \max(0,\; u_t - u_{n1})}{\pi_0 - \pi^*}"
    )
    st.markdown("""
Total unemployment cost (pp-years above $u_{n1}$) per 1 pp reduction in inflation.
Adaptive expectations → high sacrifice ratio.  Rational → zero sacrifice ratio.
    """)

    st.divider()

    st.markdown("### 8. Further Reading")
    st.markdown("""
- **Sargent, T. J. (1983)** — *Stopping Moderate Inflations*
- **Lucas, R. E. (1976)** — *Econometric Policy Evaluation: A Critique*
    """)

# =============================================================================
# TAB 3 — Quiz (interactive, button-based, immediate feedback)
# =============================================================================
with tab_quiz:
    st.markdown(
        '<h2 class="section-h">📝 Quiz — Inflation, Expectations &amp; the Bargaining Gap</h2>',
        unsafe_allow_html=True,
    )

    # ── Score summary ─────────────────────────────────────────────────────────
    _qa      = st.session_state["quiz_answers"]
    _n_done  = len(_qa)
    _n_corr  = sum(1 for oi, sel in _qa.items() if sel == QUIZ[oi]["ans"])
    _n_total = len(QUIZ)

    _score_pct = int(_n_corr / _n_total * 100) if _n_total > 0 else 0
    _grade     = (
        "Excellent 🌟" if _score_pct >= 85
        else "Good 👍"  if _score_pct >= 60
        else "Keep going 📖"
    )

    st.markdown(
        f'<div class="score-badge">'
        f'<div><span class="big">{_n_corr}/{_n_total}</span><br>'
        f'<span class="label">correct answers</span></div>'
        f'<div><span class="big">{_score_pct}%</span><br>'
        f'<span class="label">{_grade}</span></div>'
        f'<div><span class="big">{_n_done}/{_n_total}</span><br>'
        f'<span class="label">answered</span></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Reset button
    _rq_col, _ = st.columns([1, 5])
    with _rq_col:
        if st.button("↺ Reset Quiz", type="secondary", use_container_width=True):
            st.session_state["quiz_answers"] = {}
            _new_order = list(range(_n_total))
            random.shuffle(_new_order)
            st.session_state["quiz_order"] = _new_order
            st.rerun()

    st.markdown("---")

    # ── Questions ──────────────────────────────────────────────────────────────
    for _display_pos, _orig_idx in enumerate(st.session_state["quiz_order"]):
        _item = QUIZ[_orig_idx]

        # Question card header
        st.markdown(
            f'<div class="quiz-q"><h4>Q{_display_pos + 1}. {_item["q"]}</h4></div>',
            unsafe_allow_html=True,
        )

        if _orig_idx in _qa:
            # ── Feedback mode: show result ──────────────────────────────────
            _sel  = _qa[_orig_idx]
            _corr = _sel == _item["ans"]
            _sel_text  = _item["opts"][_sel]
            _corr_text = _item["opts"][_item["ans"]]

            if _corr:
                st.markdown(
                    f'<div class="quiz-correct">'
                    f'✅ <b>Correct!</b> &nbsp; {_sel_text}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="quiz-wrong">'
                    f'❌ <b>Incorrect.</b> &nbsp; You chose: {_sel_text}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="quiz-answer-correct">'
                    f'✅ <b>Correct answer:</b> &nbsp; {_corr_text}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                f'<div class="quiz-exp">💡 <b>Explanation:</b> {_item["exp"]}</div>',
                unsafe_allow_html=True,
            )

        else:
            # ── Button mode: show options as clickable buttons ──────────────
            for _opt_idx, _opt_text in enumerate(_item["opts"]):
                if st.button(
                    _opt_text,
                    key=f"q{_orig_idx}_opt{_opt_idx}",
                    use_container_width=True,
                ):
                    st.session_state["quiz_answers"][_orig_idx] = _opt_idx
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Copyright footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="copyright-footer">'
    '© Jayanta Sarkar (Queensland University of Technology, 2026) &nbsp;·&nbsp; '
    'WS/PS Labour Market &amp; Phillips Curve Simulation'
    '</div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# Animation continuation — advance one frame and rerun (runs outside all tabs)
# Placed last so all UI renders before the sleep delay.
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state["anim_running"]:
    if _frame < _anim_t_max:
        time.sleep(0.65)
        st.session_state["anim_frame"] += 1
        st.rerun()
    else:
        st.session_state["anim_running"] = False
