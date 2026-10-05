# Order-Necessity Gate v0.1.2 — audit-remediation release

**Date:** 2026-10-05

This patch release hardens the solver path identified by adversarial review. It does not change the published example values.

## Changes

- Requires a successful optimal MILP solve before reporting a point-valued restricted optimum.
- Requires solver status `0`, a finite dual bound, and a finite MIP gap no larger than the requested tolerance.
- Rejects interrupted/time-limited solves even when they return a feasible incumbent objective.
- Adds `tests/solver_certification_test.py` with regression cases for uncertified incumbents.
- Extends the smoke test to assert optimality certificates on the MILP-based published examples.
- Removes a local temporary-workspace path reference from the public validation documentation.

## Scientific status

The public examples remain unchanged:

- `ORDER_KEY_v1`: gap `0.5 bits`;
- K2: `0` on 15/15 retained points;
- REGIME high-proxy set: `0` on 26/26 retained points;
- DCR frozen grid: maximum about `0.018933608625138487 bits`.

The correction affects how future/conflict cases are certified, not the numerical values retained in the current release.
