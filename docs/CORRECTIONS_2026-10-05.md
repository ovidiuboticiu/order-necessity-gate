# Corrections — 2026-10-05

## K2 CSV schema correction

`data/k2_results.csv` contained one malformed row for `K2-T2, rho=0.1`: the `onpolicy_state_conflicts` field was omitted, leaving 10 values under an 11-column header.

The source recheck logic gives:

- `onpolicy_action_conflicts = 0`;
- `onpolicy_state_conflicts = 0`;
- `OrderNecessityGap = 0.0`.

The row was corrected by inserting the missing zero-valued state-conflict field. No reported K2 metric or scientific conclusion changed.

## REGIME public-evidence completion

The README and results documentation stated that all 26 historical REGIME points with old `G_ord >= 0.10` had a count-based policy matching the unrestricted optimum, but the clean public repository previously exposed only representative REGIME controls.

`data/regime_high_proxy_26.json` now publishes the complete retained 26-point table from the source research archive. Across those rows, the maximum absolute recorded `loss_vs_opt` is approximately `8.88e-16`, consistent with equality to float64 precision.

## Verification

Run:

```bash
python tests/data_integrity_test.py
```

This correction changes public inspectability and one CSV schema defect; it does not create a new agent result or broaden the scientific claim.

## MILP certification guard

A later adversarial audit found that the original public solver wrapper rejected a MILP result only when `result.fun is None`. A time-limited or otherwise unsuccessful solve can still return a feasible incumbent objective, so the wrapper could have reported that incumbent as `IG_best_SA` and then as a point-valued `OrderNecessityGap` without an optimality certificate.

The implementation now requires solver success, optimal status, a finite dual bound, and a finite MIP gap within the requested tolerance before accepting a point-valued restricted optimum. Otherwise it raises an error rather than certifying order necessity.

The already-published example values are unchanged; this correction hardens the method for future/conflict cases. See `tests/solver_certification_test.py` and `docs/VALIDATION.md`.
