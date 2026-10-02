# Validation

The cleaned repository was checked against the retained reference values from the source research archive.

## Smoke test

Run:

```bash
python tests/smoke_test.py
```

Expected result:

```text
PASS {'order_key_gap': 0.5, 'dcr_max': (0.018933608625138487, 0.8, 0.95, 0.1), 'k2_gap': 0.0, 'regime_gap': 0.0}
```

The test checks four representative cases:

- **ORDER_KEY_v1:** `OrderNecessityGap = 0.5`;
- **DCR frozen grid:** maximum gap `0.018933608625138487` at `r=.80, q_hi=.95, h=.10`;
- **K2-T2, rho=.75:** historical `AdaptiveGap=0.07371004163477379`, but `OrderNecessityGap=0`;
- **REGIME representative high-proxy case:** `OrderNecessityGap=0`.

## Integrity

The public code is self-contained and does not depend on:
- private repository paths;
- local `/mnt/data` paths;
- historical ZIP bundles;
- uncommitted result files.

The public tree is intentionally smaller than the private provenance archive.

## Interpretation

Passing the smoke test validates consistency with the retained reference calculations. It is not a claim of peer review, external validation, or broad empirical generalization.
