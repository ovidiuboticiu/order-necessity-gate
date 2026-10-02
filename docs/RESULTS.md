# Results

## Summary

The retained examples separate three qualitatively different cases.

| Case | Structural class | Main result |
|---|---|---:|
| K2 | on-policy representable | gap = 0 |
| REGIME | on-policy representable | gap = 0 on old high-proxy points |
| DCR | nonrepresentable but cheap | max gap = 0.018933608625138487 |
| ORDER_KEY_v1 | nonrepresentable + non-bypassable | gap = 0.5 |

## K2

The historical K2 grid had adaptive advantage over open-loop, with maximum:

`AdaptiveGap = 0.07371004163477379 bits`.

But retrospective Order-Necessity analysis found:

- 15/15 points: zero on-policy `S_A` action conflicts;
- 15/15 points: the unrestricted optimum is reproducible by a restricted count-based policy;
- therefore 15/15 have `OrderNecessityGap = 0`.

Interpretation:

`adaptive value != order-specific value`.

## REGIME

A weaker historical proxy made 26 points look promising, including values above `0.10 bits`.

Under the stronger restricted-policy control:

- 26/26 old high-proxy points are on-policy representable in `Pi_S`;
- therefore their exact `OrderNecessityGap = 0`.

Representative case:

- `hi=.95, lo=.50, r=.95, h=.12, W=5`;
- `IG_opt = 0.7713565820675281`;
- old proxy `G_ord = 0.10048364768991935`;
- `IG_best-S_A = IG_opt`;
- exact gap = `0`.

Three other conflict controls have tiny positive gaps around `2.8e-4 bits`.

Interpretation:

`dynamic latent structure != order-necessary probe selection`.

## DCR

DCR was designed to create real same-`S_A` order conflicts.

All 27 frozen points have genuine on-policy order sensitivity, but all fail the retained `0.10-bit` gate.

Maximum:

- `r=.80`;
- `q_hi=.95`;
- `h=.10`;
- `IG_opt = 0.4455751271123113`;
- `IG_best-S_A = 0.4266415184871728`;
- `OrderNecessityGap = 0.018933608625138487 bits`.

The key structural observation is bypassability.

At `r=.95, q_hi=.95, h=.40`:
- forcing the order-aware route would create collision cost `0.12339999589818847 bits`;
- but a legal restricted-policy bypass costs only `0.0006464874418642408 bits`;
- therefore the global gap remains tiny.

Interpretation:

`large local conflict != large global restriction cost`.

## ORDER_KEY_v1

Synthetic positive control:

- `IG_opt = 1`;
- `IG_best-S_A = 0.5`;
- `OrderNecessityGap = 0.5 bits`.

ORDER_KEY combines:
- large collision mass;
- incompatible action requirements;
- substantial local regret;
- no cheap bypass.

It demonstrates that a large Order-Necessity gap is mathematically possible under the gate.

It is a synthetic control, not evidence that similarly large gaps occur in more natural adaptive-sensing tasks.

## Reproduction

Run:

```bash
python tests/smoke_test.py
```

The clean release candidate reproduces:
- ORDER_KEY gap = `0.5`;
- DCR frozen-grid maximum = `0.018933608625138487`.
