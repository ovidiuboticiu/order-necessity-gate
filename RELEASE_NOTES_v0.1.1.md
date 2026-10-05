# Order-Necessity Gate v0.1.1 — correction release

**Date:** 2026-10-05

This patch release improves public-data integrity and inspectability without changing the methodological result.

## Changes

- Fixed the malformed `K2-T2, rho=0.1` row in `data/k2_results.csv` by restoring the missing zero-valued `onpolicy_state_conflicts` field.
- Published `data/regime_high_proxy_26.json`, the complete retained 26-point table supporting the public `26/26` REGIME statement.
- Added `tests/data_integrity_test.py` to check the K2 CSV schema and completeness/numerical consistency of the 26-point REGIME table.
- Added `AI_USE.md` describing substantial AI assistance and the human responsibility boundary.
- Added `docs/CORRECTIONS_2026-10-05.md`.

## Scientific status

The core result is unchanged: K2 and the historical high-proxy REGIME points do not require ordered history under the tested restricted-policy criterion; DCR has a small positive gap; ORDER_KEY_v1 remains a synthetic positive control.
