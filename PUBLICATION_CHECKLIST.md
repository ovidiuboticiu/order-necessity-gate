# Public-release checklist

## Content

- [x] Clear public-facing README.
- [x] Method separated from project history.
- [x] Results summarized without overstating H1.
- [x] Limitations explicit.
- [x] No novelty/priority claim.
- [x] No confirmatory-agent claim.
- [x] Synthetic positive control identified as synthetic.
- [x] Negative results retained.
- [x] Historical `0.10-bit` threshold identified as protocol-specific.

## Reproducibility

- [x] Self-contained core implementation.
- [x] No dependency on private repository paths.
- [x] No `/mnt/data` or local-machine path dependency.
- [x] NumPy/SciPy dependencies declared.
- [x] Smoke test reproduces ORDER_KEY gap `0.5`.
- [x] Smoke test reproduces DCR grid max `0.018933608625138487`.
- [x] Smoke test reproduces K2 adaptive-gap reference while certifying order-necessity gap 0.
- [x] Smoke test reproduces representative REGIME order-necessity gap 0.

## Data

- [x] DCR frozen 27-point decomposition included.
- [x] K2 retrospective 15-point table included.

## Before publication

- [ ] Select license.
- [ ] Create clean GitHub repository, suggested name: `order-necessity-gate`.
- [ ] Copy only this release-candidate tree into the new repository root.
- [ ] Run smoke test once from the new repository.
- [ ] Confirm repository description/topics.
- [ ] Switch private -> public only after final inspection.

## Suggested repository description

> A finite-horizon gate for testing whether ordered interaction history is genuinely necessary for optimal adaptive information seeking.

## Suggested topics

`ai-agents`, `information-gain`, `adaptive-sensing`, `pomdp`, `decision-making`, `evaluation`, `research`
