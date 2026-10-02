# Limitations

## Scientific scope

This repository is a methodological artifact, not a completed agent-learning study.

No confirmatory neural agent was run under the final protocol.

The broader hypothesis that an agent can or cannot generalize epistemic behavior to a structurally novel uncertainty regime therefore remains untested here.

## Model scope

The included implementation assumes:
- finite horizon;
- binary observations;
- binary terminal target;
- three probe actions in the retained examples;
- exact finite latent enumeration;
- terminal entropy as the objective.

The conceptual decomposition is broader than these implementation choices, but the included solver is not presented as a universal-purpose framework.

## Threshold

The `0.10-bit` threshold used in the historical source project was a protocol choice.

It is not claimed to be:
- universal;
- natural;
- theoretically privileged;
- appropriate for every task.

The public artifact preserves results relative to that historical threshold but does not recommend it as a general standard.

## Zero-conflict certificate

The implemented deterministic tie-broken zero-conflict certificate is sufficient for gap zero.

It is not a complete iff test in the presence of action ties. A stronger future implementation could work with the full set of zero-regret actions at each history.

## Numerical implementation

The public solver uses:
- NumPy float64;
- SciPy MILP;
- explicit finite-tree enumeration.

The source research program additionally used independent implementations and exact/Fraction checks for selected controls. The clean release keeps the core method small rather than reproducing every historical audit artifact.

## External validity

ORDER_KEY is deliberately synthetic.

DCR, K2, and REGIME are small constructed information-seeking families.

Results from these tasks should not be generalized directly to:
- long-horizon agents;
- natural-language agents;
- real-world tool use;
- arbitrary memory architectures.

## Novelty

No priority or novelty claim is made.

A literature review would be required before making claims about originality relative to controlled sensing, POMDP policy compression, information acquisition, memory-constrained policies, or adjacent work.
