# Public-release candidate audit

**Status:** PASS WITH ONE MANUAL DECISION  
**Date:** 2 October 2026  
**Candidate path:** `16_public_release_candidate/`

## Scope

This audit asks whether the cleaned tree is suitable to become a separate public GitHub repository without exposing the full internal research archive.

## Content audit

### PASS — signal is clear

The candidate has one central methodological object:

`OrderNecessityGap = IG_opt-order-aware - IG_best-S_A-policy`.

The README explains:
- the question;
- the metric;
- the Bellman-regret interpretation;
- representative positive and negative cases;
- what is and is not claimed.

Historical redesign chronology, recovery notes, abandoned families, and administrative material are omitted.

### PASS — negative results are not hidden

The candidate preserves:
- K2: order-necessity gap 0 despite adaptive value;
- REGIME: high weak-proxy values but exact gap 0 on representative/high-proxy points;
- DCR: genuine order dependence but maximum frozen gap only ~0.01893;
- ORDER_KEY: synthetic positive control with gap 0.5.

### PASS — no agent overclaim

The release states explicitly that:
- no confirmatory neural-agent experiment was run;
- the broader epistemic-generalization hypothesis was not tested or rejected;
- the artifact is methodological.

### PASS — no novelty overclaim

The release makes no priority claim and explicitly notes that a literature review is required before originality claims.

## Reproducibility audit

A clean local copy of the staged implementation was executed with the declared NumPy/SciPy dependencies.

Observed smoke-test result:

`PASS {'order_key_gap': 0.5, 'dcr_max': (0.018933608625138487, 0.8, 0.95, 0.1), 'k2_gap': 0.0, 'regime_gap': 0.0}`

This reproduces the retained reference values for all four showcased cases.

The candidate has no dependency on:
- `/mnt/data`;
- the private repository layout;
- historical ZIP bundles;
- uncommitted JSON files.

## Scope/maintainability audit

The public code intentionally remains small:
- finite latent enumeration;
- binary observations and binary target;
- three-action examples;
- SciPy MILP for global best-`S_A`.

This limitation is explicit in `docs/LIMITATIONS.md`.

## Data audit

Included:
- full 27-point DCR frozen decomposition;
- full 15-point K2 retrospective table;
- compact REGIME control values.

## Remaining manual decision

### LICENSE — unresolved

No license was selected automatically.

This must be decided before publication because it changes third-party reuse rights.

See `LICENSE_DECISION_REQUIRED.md`.

## Publication disposition

**Technically ready to extract into a new repository.**

Suggested repository name:

`order-necessity-gate`

Suggested sequence:
1. create the new repository as **private**;
2. copy only the contents of `16_public_release_candidate/` into its root;
3. choose the license;
4. run `python tests/smoke_test.py` once in the new repository;
5. inspect the rendered README;
6. only then switch private -> public.

The original full research repository should remain private as the provenance archive.
