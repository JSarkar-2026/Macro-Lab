# WS/PS Labour Market & Phillips Curve

### An Interactive Macroeconomics Simulation

This simulation lets students explore how wages, prices, and inflation are connected
through the labour market — and how central bank policy shapes the adjustment path
after an economic shock. It is designed for use in intermediate and advanced
macroeconomics courses.

---

## What This Simulation Shows

The model has three interacting parts:

**1. The Labour Market (WS/PS)**
Workers and firms bargain over the real wage. The *Wage-Setting (WS) curve* is
upward-sloping in employment: when jobs are plentiful, workers bargain for higher wages.
The *Price-Setting (PS) line* is flat: it shows the maximum real wage firms can afford
given their markup. Where WS meets PS is the labour market equilibrium — the *natural
rate of unemployment* u_n and the employment rate e*.

**2. The Bargaining Gap (BG)**
When employment is above e*, workers can push wages above what firms planned. Firms pass
this cost into prices. The resulting *Bargaining Gap* — (w_WS − w_PS) / w_PS — drives
inflation above expected inflation. A negative gap (employment below e*) creates
downward pressure, but wages are downwardly rigid: the disinflationary effect is weaker
than the inflationary effect of an equal positive gap. This produces the empirically
observed *asymmetric curvature* of the Phillips curve.

**3. Inflation Expectations and the Short-Run Phillips Curve (SRPC)**
Inflation expectations adapt with a one-period lag: agents expect this period's inflation
to equal last period's. Each time expectations ratchet up, the SRPC shifts upward. The
successive SRPCs trace out the Long-Run Phillips Curve (LRPC) — a vertical line at the
natural rate — illustrating why there is no permanent trade-off between unemployment and
inflation.

---

## Learning Objectives

By the end of a session with this simulation, students should be able to:

1. Explain why the Bargaining Gap, not unemployment itself, drives inflation.
2. Trace the full adjustment path after a supply shock (markup or bargaining power
   change) from the WS/PS diagram through the SRPC to the time series.
3. Explain why the Short-Run Phillips Curve is kinked at the natural rate (asymmetric
   curvature).
4. Distinguish between a *movement along* the SRPC (caused by aggregate demand
   fluctuations) and a *shift of* the SRPC (caused by changing inflation expectations).
5. Demonstrate the Lucas Critique: compare the costly, gradual disinflation under
   adaptive expectations with the costless adjustment under rational expectations.
6. Explain why an oil price shock produces stagflation (simultaneously higher
   unemployment and higher inflation).

---

## The Three Types of Shock

### Supply Shocks — WS/PS shifts

Shocks that permanently change the labour market equilibrium.

| Shock | Slider | Effect |
| --- | --- | --- |
| Markup increase | Firm markup μ ↑ | PS line shifts down → new lower e*, higher u_n → stagflation |
| Oil price rise | Oil price shock ↑ | Same as markup increase (raises effective μ) |
| Workers' bargaining power | WS intercept b ↑ | WS curve shifts up → new lower e*, higher u_n → stagflation |

**Adjustment path**: At old e*, the BG is now positive. Inflation rises above π^e.
As expectations catch up, the SRPC shifts upward along the initial LRPC₀. The central
bank (if φ > 0) raises unemployment toward the new u_n. The SRPC family traces the
stagflation path.

### Demand Shock — movement along the SRPC

The AD demand shock slider shifts employment *along* the existing WS and PS curves
without moving them.

- **Positive (boom)**: unemployment falls below u_n → employment rises above e* →
  positive BG → inflation rises in period 1. The economy moves *along* the SRPC.
  From period 2, expectations adjust and the SRPC shifts upward.
- **Negative (slump)**: the opposite — disinflation through a negative BG.

### Oil Price Shock — adverse or favourable supply

- Positive value (+10% to +20%): oil price rise → effective markup rises → PS shifts
  down → stagflation (higher inflation and higher u_n simultaneously).
- Negative value (−10% to −20%): oil price fall → PS shifts up → disinflationary
  supply improvement.

---

## Using the Simulation

### How the Animation Works

Shift any parameter slider and the simulation **animates automatically** through the
adjustment path — no manual time-stepping required.

- With **φ = 0** (default, fully accommodating CB): the animation always runs all
  10 periods, showing how inflation spirals as expectations adapt.
- With **φ > 0** (CB active): the animation stops as soon as unemployment converges
  within 0.2 pp of the new natural rate u_n₁, which may occur before period 10.

Use the four control buttons at the top of the Simulation tab:

| Button | Action |
| --- | --- |
| ▶ Play | Restart from t = 0 |
| ⏸ Pause | Freeze at current period |
| ⏮ Reset | Return to t = 0 |
| ⏭ Final | Jump to last period |

### Suggested Learning Sequence

**Step 1 — Confirm the baseline (all sliders at default)**
The economy is at its initial equilibrium: e*₀ ≈ 85.3%, u_n₀ ≈ 14.7%, inflation = π* = 2%.
The Bargaining Gap is zero. Press ▶ Play — nothing changes across all 10 periods.
This confirms the model is in steady state.

**Step 2 — Apply a markup shock**
Increase Firm markup μ from 0.30 to 0.40. The animation starts immediately:

- PS line shifts down in the WS/PS diagram; a Bargaining Gap opens at e*₀.
- New equilibrium e*₁ and u_n₁ appear on the diagram.
- Inflation jumps in period 1 and continues to rise as π^e adapts.
Watch the coloured dot track the economy's employment position each period.

**Step 3 — Add an AD demand shock**
Reset markup to 0.30. Set AD demand shock to +6. The green employment marker shows
where the economy sits along the PS line — BG > 0, but WS and PS have not moved.
From period 2, expectations adjust and the SRPC shifts upward along LRPC₀.

**Step 4 — Explore CB response**
With any shock active, raise Policy intensity φ (try 2.0–4.0). Higher φ means the CB
tightens more aggressively in response to above-target inflation, pushing unemployment
toward the new u_n. The animation stops at convergence.

**Step 5 — Rational expectations (Lucas Critique)**
With a markup shock active and φ > 0, switch Expectations from *Adaptive* to *Rational*.
Under rational expectations, agents immediately anticipate the adjustment: the SRPC
collapses to a single shift and disinflation is costless. This is the Lucas Critique.

---

## Panel Guide

| Panel | What it shows |
| --- | --- |
| **WS/PS Labour Market** | Wage-setting and price-setting curves; equilibrium e*; Bargaining Gap arrow; animated economy dot; AD shock point |
| **Phillips Curve (e, π)** | SRPC family accumulating period by period; economy path; amber dot = current period; LRPC₀ vertical reference |
| **Time Series** | Inflation π and expectations π^e (top); unemployment u vs. natural rate u_n (bottom); dashed lines for u_n₀ and u_n₁ |

---

## Key Parameters at a Glance

| Parameter | Default | Role |
| --- | --- | --- |
| WS intercept b | 0.30 | Workers' outside option; shock = move above 0.30 |
| Firm markup μ | 0.30 | Price-cost margin; shock = move above 0.30 |
| Oil price shock | 0% | Adverse/favourable cost shock |
| AD demand shock | 0 | Demand boom (+) or slump (−) |
| Slope α | 0.1 | Inflation sensitivity to Bargaining Gap |
| Inflation target π* | 2% | Central bank's announced goal |
| Policy intensity φ | 0.0 | CB reaction strength; 0 = fully accommodating |

---

## Technical Notes

- Built with Python 3.10+, Streamlit, NumPy, Pandas, Plotly.
- The model uses NumPy vectorisation for all calculations.
- Adaptive expectations use λ = 1 (full one-period lag) as the baseline.
- The Bargaining Gap is normalised: BG = (w_WS − w_PS) / w_PS, measured in
  percentage points when multiplied by 100.
- Downward wage rigidity is parameterised by β = 0.5: a negative BG passes through
  at half the rate of a positive BG of the same magnitude.
- Animation: parameter changes trigger automatic playback from t = 0; the full
  dataset (11 rows) is cached and sliced to the current frame on each rerun.
- Run locally: `streamlit run app.py` from the `Phillips-Curve/` directory.

---

## Further Reading

- **Sargent, T. J. (1983)** — *Stopping Moderate Inflations*
- **Lucas, R. E. (1976)** — *Econometric Policy Evaluation: A Critique*
- **Shapiro, C. & Stiglitz, J. E. (1984)** — *Equilibrium Unemployment as a Worker
  Discipline Device*, American Economic Review
