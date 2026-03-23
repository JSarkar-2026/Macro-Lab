# Instructor / Developer Instructions

## WS/PS Labour Market & Phillips Curve Simulation

This document explains how to adjust the simulation's parameters, slider settings,
and model calibration. All changes are made in two files:

- **`app.py`** — Streamlit interface, animation logic, sliders, charts, quiz
- **`model.py`** — Economic model engine (equations, simulation loop)

---

## 1. Fixed Constants (Hidden from Students)

These are hard-coded in `app.py` near the top of the model constants block
(around line 450). They define the **pre-shock baseline equilibrium** at t=0
and are never exposed as sliders.

| Constant | Variable | Current Value | What it controls |
| --- | --- | --- | --- |
| WS slope | `_GAMMA` | `0.55` | Steepness of the Wage-Setting curve. Higher → steeper WS, lower e*, higher u_n |
| Downward wage rigidity | `_BETA` | `0.5` | Asymmetric PC curvature. β=1 → symmetric; β<1 → wages fall less than they rise |
| Adaptive expectations speed | `_LAMBDA` | `1.0` | Speed of expectation updating. λ=1 → π^e_t = π_{t−1} (full one-period lag) |
| Baseline WS intercept | `_B0` | `0.3` | Pre-shock workers' outside option. Defines t=0 equilibrium |
| Baseline markup | `_MU0` | `0.3` | Pre-shock firm markup. Defines t=0 equilibrium |
| Maximum animation periods | `_T_MAX` | `10` | Number of periods shown during animation |

**Derived baseline equilibrium** (auto-computed from the above):

- w_PS₀ = 1 / (1 + μ₀) ≈ 0.769
- e*₀ = (w_PS₀ − b₀) / γ ≈ 85.3%
- u_n₀ = (1 − e*₀) × 100 ≈ 14.7%

### How to change a fixed constant

Open `app.py` and edit the value directly, e.g.:

```python
_GAMMA = 0.60   # was 0.55 — makes WS steeper, raises u_n
_B0    = 0.25   # was 0.30 — lowers WS intercept, lowers u_n
```

**Important**: If you change `_B0`, also update the `b_ws` slider's **default value**
(3rd argument) to match, so the "no shock" baseline remains consistent.
Similarly, if you change `_MU0`, update the `mu_markup` slider's default.

To increase the maximum number of animation periods, change `_T_MAX`:

```python
_T_MAX = 15   # was 10 — allows up to 15 adjustment periods
```

The full dataset is always computed up to `_T_MAX + 1` rows and sliced
to the current animation frame.

---

## 2. Animation System

The simulation is **fully animated**: there is no manual time-period slider.
When a student moves any parameter slider, the animation starts automatically
from t = 0.

### How it works

1. Every slider change is detected via a parameter hash stored in
   `st.session_state["last_param_hash"]`.
2. On detecting a change, `anim_frame` resets to 0 and `anim_running` is set
   to `True`.
3. At the end of each script run, if `anim_running = True` and
   `anim_frame < anim_t_max`, the script sleeps for 0.65 seconds, increments
   the frame, and calls `st.rerun()`.
4. The simulation DataFrame (`df_full`, always `_T_MAX + 1` rows) is
   pre-computed and cached. Each frame slices `df_full.iloc[:frame + 1]`
   for display.

### Animation end condition

| Condition | End period |
| --- | --- |
| φ = 0 (no CB response) | Always `_T_MAX` (10 by default) |
| φ > 0 (CB active) | First period t where \|u_t − u_n₁\| < 0.2 pp, or `_T_MAX` |

To change the convergence tolerance (0.2 pp), edit `_find_t_max()` in `app.py`:

```python
tol = 0.2   # change to e.g. 0.1 for tighter convergence criterion
```

### Animation speed

The inter-frame delay is 0.65 seconds, set at the very end of `app.py`:

```python
time.sleep(0.65)   # change to 0.4 (faster) or 1.0 (slower)
```

### Manual animation controls

Students can use four buttons at the top of the Simulation tab:

| Button | Action |
| --- | --- |
| ▶ Play | Restart animation from t = 0 |
| ⏸ Pause | Stop at current frame |
| ⏮ Reset | Return to t = 0, paused |
| ⏭ Final | Jump to last period, paused |

---

## 3. Welcome / How-to-Run Page

The app opens on a **welcome page** (before the simulation tabs). This page:

- Explains what the simulation shows
- Describes how the animation works
- Lists the six suggested scenarios
- Provides a quick-reference slider table and panel guide

Students click **"▶ Enter Simulation"** to proceed. The state is stored in
`st.session_state["intro_complete"]`.

The sidebar always has a **"📖 How to Run"** button that returns to this page
from within the simulation.

To **remove the welcome page** entirely and go straight to the simulation,
delete the `if not st.session_state["intro_complete"]:` block and remove
`"intro_complete"` from `_defaults`. Also remove the `📖 How to Run` sidebar
button.

To **edit the welcome page content**, find the block starting with:

```python
if not st.session_state["intro_complete"]:
```

in `app.py` (around line 350). All content is in standard Streamlit markdown
and `st.markdown()` calls within that block.

---

## 4. Slider Reference

Each slider is defined by four numbers: `(min, max, default, step)`.
All sliders are in `app.py` inside the `with st.sidebar:` block.

### Labour Market

#### WS intercept b

```python
b_ws = st.slider("WS intercept b", 0.1, 0.6, 0.3, 0.05)
```

| Setting | Value | Notes |
| --- | --- | --- |
| Min | 0.1 | Very low outside option |
| Max | 0.6 | High bargaining power; WS may not intersect PS |
| Default | 0.3 | Must equal `_B0` — no shock at default |
| Step | 0.05 | — |

The shock is `Δb = b_ws − _B0`. Moving above 0.3 creates a positive WS shift.

#### AD demand shock

```python
delta_AD_u = st.slider("AD demand shock", -10.0, 10.0, 0.0, 1.0)
```

| Setting | Value | Notes |
| --- | --- | --- |
| Min | −10.0 | Strong demand contraction |
| Max | +10.0 | Strong demand boom |
| Default | 0.0 | No AD shock |
| Step | 1.0 | — |

Internally applied as `−2 × delta_AD_u` in the unemployment equation
(the factor of 2 amplifies the BG effect to match markup shock sensitivity).
To adjust sensitivity, change the multiplier in `model.py`:

```python
u_t = max(0.01, min(30.0, u_n_pre + p.phi * (pie_t - p.pi_star) - 2.0 * p.delta_AD_u))
```

Change `2.0` to `3.0` for higher sensitivity, or `1.0` for lower.

#### Firm markup μ

```python
mu_markup = st.slider("Firm markup μ", 0.1, 0.8, 0.3, 0.05)
```

| Setting | Value | Notes |
| --- | --- | --- |
| Min | 0.1 | Low markup, high PS wage |
| Max | 0.8 | Very high markup; PS wage drops substantially |
| Default | 0.3 | Must equal `_MU0` — no shock at default |
| Step | 0.05 | — |

#### Oil price shock (% change)

```python
delta_oil = st.slider("Oil price shock (% change)", -0.20, 0.20, 0.0, 0.02)
```

| Setting | Value | Notes |
| --- | --- | --- |
| Min | −0.20 | −20%: favourable oil shock (PS shifts up) |
| Max | +0.20 | +20%: adverse oil shock (PS shifts down) |
| Default | 0.0 | No oil shock |
| Step | 0.02 | — |

Internally, `mu_eff = mu_markup + delta_oil`. The oil shock is treated
identically to a markup change — both shift the PS curve.

---

### Phillips Curve

#### Slope α

```python
alpha = st.slider("Slope α", 0.1, 1.0, 0.1, 0.05)
```

| Setting | Value | Notes |
| --- | --- | --- |
| Min | 0.1 | Flat SRPC — sluggish inflation response |
| Max | 1.0 | Steep SRPC — 1% BG → 1 pp inflation above π^e |
| Default | 0.1 | Calibrated for visible but gradual dynamics |
| Step | 0.05 | — |

**Stability constraint**: α × γ × φ / w_PS < 1. The app shows a warning when
violated.

---

### Central Bank

#### Inflation target π*

```python
pi_star = st.slider("Inflation target π* (%)", 0.0, 8.0, 2.0, 0.5)
```

| Setting | Value | Notes |
| --- | --- | --- |
| Default | 2.0% | Standard central bank target |
| Range | 0–8% | — |

#### Policy intensity φ

```python
phi = st.slider("Policy intensity φ", 0.0, 8.0, 0.0, 0.25)
```

| Setting | Value | Notes |
| --- | --- | --- |
| Min | 0.0 | Fully accommodating CB (default) |
| Max | 8.0 | Strong activist CB |
| Default | 0.0 | φ = 0 is the pedagogically clean starting point |
| Step | 0.25 | — |

The CB reaction rule is: `u_t = u_n_pre + φ × (π^e_t − π*)`.

- φ = 0: CB ignores inflation — employment stays at e*₀, inflation spirals upward.
- φ ≈ 4: unemployment converges toward the new u_n within the 10-period window
  for typical shocks, without overshooting.

To change the default:

```python
phi = st.slider("Policy intensity φ", 0.0, 8.0, 4.0, 0.25)  # default = 4.0
```

---

## 5. Model Equations (Summary)

### Labour Market Equations

- WS curve: w_WS(e) = b + γ·e
- PS level: w_PS = 1 / (1 + μ)
- Equilibrium: e* = (w_PS − b) / γ, u_n = (1 − e*) × 100
- Bargaining Gap: BG = (w_WS(e) − w_PS) / w_PS (normalised fraction)

### Phillips Curve Equation

- Adaptive expectations: π^e_t = π_{t−1} (λ = 1)
- Inflation: π_t = π^e_t + α × scale × BG_t × 100
  - scale = 1.0 if BG ≥ 0 (positive gap, full pass-through)
  - scale = β if BG < 0 (negative gap, downward wage rigidity)

### CB Reaction

- u_t = u_n_pre + φ × (π^e_t − π*) − 2 × delta_AD_u

### Stability Condition

- α × γ × φ / w_PS < 1 (required for non-oscillatory convergence)

---

## 6. Changing Sensitivity

| What to change | Where | How |
| --- | --- | --- |
| BG response to markup/b shocks | `_GAMMA` in `app.py` | Increase (e.g. 0.55 → 0.65) |
| BG response to AD shock | Multiplier in `model.py` CB rule | Increase (e.g. `2.0` → `3.0`) |
| Inflation response to BG | `alpha` slider default | Increase default (e.g. 0.1 → 0.3) |
| Speed of adjustment | `phi` slider default | Increase default (e.g. 0.0 → 4.0) |
| Oil shock range | `delta_oil` slider min/max | Change (e.g. −0.20/+0.20 → −0.30/+0.30) |
| Asymmetry of PC curvature | `_BETA` in `app.py` | Decrease (more asymmetric); 1.0 = symmetric |
| Animation speed | `time.sleep(0.65)` at end of `app.py` | Decrease (faster) or increase (slower) |
| Maximum animation periods | `_T_MAX` in `app.py` | Increase (e.g. 10 → 15) |
| Convergence tolerance (CB) | `tol = 0.2` in `_find_t_max()` | Tighten (e.g. 0.2 → 0.1) |

---

## 7. Running the App Locally

```bash
cd "Phillips-Curve"
pip install -r requirements.txt
streamlit run app.py
```

The app runs at `http://localhost:8501` by default.

## 8. Deployment (Streamlit Community Cloud)

1. Push the `Phillips-Curve/` folder to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. Set the main file path to `Phillips-Curve/app.py`.
4. Replace the `GA_ID = "G-XXXXXXXXXX"` placeholder in `app.py` with your
   Google Analytics tag before deploying.

See `DEPLOYMENT.md` for step-by-step instructions.
