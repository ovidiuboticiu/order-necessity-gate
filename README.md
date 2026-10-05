# Order-Necessity Gate for Adaptive Information Seeking

**A structural test for a simple question: does an adaptive system truly need the order of its past observations, or would a compressed count-based history be enough?**

**Status:** public methodological release; correction release v0.1.2 published  
**Type:** methodological research artifact  
**Scope:** finite-horizon adaptive information seeking with binary observations  
**Novelty claim:** none

**Correction release:** v0.1.2 additionally hardens the MILP path: a point-valued `OrderNecessityGap` is reported only when the solver returns a certified optimum within the requested MIP-gap tolerance. The published example values are unchanged.

## In one minute

Imagine two histories containing the same observations but in a different order. If both can always lead to an equally good next decision, then the apparent order sensitivity is not actually necessary. If compressing those histories together forces a measurable loss, order really matters.

The **Order-Necessity Gate** measures that loss by comparing the unrestricted optimum with the best policy that only sees a compressed action-observation count statistic.

**Main empirical picture.** The positive control produced an `OrderNecessityGap` of **0.5 bits**. Earlier K2 and REGIME cases that looked order-sensitive produced a gap of **0**, while the frozen DCR grid reached only about **0.0189 bits**.

**Practical use.** This gate is intended to screen candidate environments *before* spending compute on a neural agent. It can reveal that a supposedly order-dependent task is structurally solvable without retaining ordered history.

**Solver-safety note.** For conflict cases, the implementation now refuses to report a point-valued gap unless SciPy/HiGHS reports a successful optimal solve, a finite dual bound, and a finite MIP gap no larger than the requested tolerance. A feasible incumbent from an interrupted solve is not treated as the optimum.

## Why this exists

Adaptive behavior can look order-sensitive without actually requiring ordered history.

A system may:
- react to feedback;
- operate in a dynamic latent environment;
- change actions when histories are permuted;
- even face local action conflicts;

and still admit an order-blind/count-based policy that matches the unrestricted optimum.

This repository isolates that distinction with an **Order-Necessity Gate**.

The central quantity is:

`OrderNecessityGap = IG_opt-order-aware - IG_best-S_A-policy`

where `S_A` is an action-observation count statistic and the restricted policy may choose probes only as a function of `S_A`.

## Core result

For finite-horizon terminal-entropy objectives:

`OrderNecessityGap = min_(pi in Pi_S) E_pi[sum_t delta*(h_t, pi(S_A(h_t)))]`

where:

`delta*(h,a) = Q*(h,a) - V*(h) >= 0`.

Interpretation:

> the gap is the minimum cumulative Bellman regret forced by compressing ordered history into the restricted statistic `S_A`.

This makes four structural issues explicit:

1. **representability** — can a restricted policy reproduce the unrestricted optimum on its own support?
2. **collision mass** — how much probability reaches histories collapsed into the same `S_A`?
3. **local action regret** — how costly is the common action forced inside that class?
4. **bypassability** — can the restricted policy reroute around the conflict cheaply?

## Main empirical examples

| Case | Result |
|---|---:|
| ORDER_KEY_v1 positive control | `OrderNecessityGap = 0.5 bits` |
| K2 retrospective grid | `0` on 15/15 points |
| REGIME old high-proxy points | `0` on 26/26 points |
| DCR frozen grid | max `0.018933608625138487 bits` |

DCR is the most informative negative example: it has genuine on-policy order-dependent action conflicts, but the globally optimal restricted policy can often reroute cheaply.

## What this repository does not claim

This is **not**:
- a demonstration that an AI agent learned epistemic generalization;
- a proof that such generalization is impossible;
- a general benchmark for all forms of memory;
- a claim that `0.10 bits` is a universal or natural threshold;
- a priority/novelty claim over prior literature.

No confirmatory neural-agent experiment was run in the source research program.

## Quick start

Requirements:

```bash
python -m pip install -r requirements.txt
```

Run the smoke test and public-data integrity check:

```bash
python tests/smoke_test.py
python tests/data_integrity_test.py
python tests/solver_certification_test.py
```

Expected final line:

```text
PASS {'order_key_gap': 0.5, 'dcr_max': (0.018933608625138487, 0.8, 0.95, 0.1), 'k2_gap': 0.0, 'regime_gap': 0.0}
```

This verifies:
- the ORDER_KEY positive-control gap of `0.5`;
- the frozen DCR-grid maximum of `0.018933608625138487` at `r=.80, q_hi=.95, h=.10`;
- K2-T2 at `rho=.75`: historical `AdaptiveGap=0.07371004163477379` but `OrderNecessityGap=0`;
- the representative REGIME high-proxy case has `OrderNecessityGap=0`.

## Repository structure

```text
src/
  core.py
  order_necessity_gate.py

examples/
  models.py

tests/
  smoke_test.py
  data_integrity_test.py
  solver_certification_test.py

data/
  dcr_grid.csv
  k2_results.csv
  regime_controls.csv
  regime_high_proxy_26.json

docs/
  METHOD.md
  RESULTS.md
  LIMITATIONS.md
  PROVENANCE.md
  VALIDATION.md

requirements.txt
AI_USE.md
LICENSE
```

## Suggested prospective screening order

Before running an agent:

`AdaptiveGap -> representability -> cheap bypass -> structural lower bound -> exact solver -> agent`

The purpose is to eliminate structurally uninformative environments before spending compute on learning systems.

## Reproducibility note

The public code is a cleaned, self-contained extraction of the frozen Order-Necessity implementation and the final structural analysis. It deliberately omits the long internal history of abandoned candidate families and archival recovery work.

The implementation was smoke-tested against the retained reference values. The complete 26-point historical REGIME high-proxy set supporting the `26/26` zero-gap statement is published in `data/regime_high_proxy_26.json`. The 2026-10-05 public-data corrections are documented in `docs/CORRECTIONS_2026-10-05.md`. See `docs/VALIDATION.md`.

## AI assistance

This project was developed with substantial AI assistance. See `AI_USE.md` for the contribution and responsibility disclosure.

## License

MIT. See `LICENSE`.
