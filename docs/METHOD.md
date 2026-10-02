# Method

## 1. Setup

Let `h_t` be the full ordered interaction history before probe decision `t`.

Let the terminal binary target be `Y).

Define terminal cost:

`C(h_W) = H(Y | h_W)`.

For any probing policy `pi`:

`J(pi) = E_pi[C(h_W)]`

and:

`IG(pi) = H(Y) - J(pi)`.

Let:
- `pi*` be the unrestricted, order-aware Bayes-optimal policy;
- `S_A(h)` be the action-observation count statistic;
- `Pi_S` be the class of policies whose probe choice depends only on `S_A(h)`;
- `pi_S*` be the best policy in `Pi_S`.

Then:

`OrderNecessityGap = IG(pi*) - IG(pi_S*) = J(pi_S*) - J(pi*)`.

## 2. Restricted statistic

For three actions and binary observations:

`S_A(h) = (n_00,n_01,n_10,n_11,n_20,n_21)`.

The restriction applies to **probe selection**. The terminal Bayesian evaluator may still use the full ordered terminal history.

This is important: the gate asks whether order is necessary to choose probes, not whether order can ever matter to inference.

## 3. Bellman decomposition

Define unrestricted-optimal cost-to-go:

`V*(h_t) = min_pi E[C(h_W) | h_t, pi]`.

Define:

`Q*(h_t,a) = E[V*(h_(t+1)) | h_t,a]`.

Local unrestricted-optimal regret is:

`delta*(h_t,a) = Q*(h_t,a) - V*(h_t) >= 0`.

For any policy `pi`:

`J(pi)-J(pi*) = E_pi[sum_t delta*(h_t,a_t)]`.

Therefore:

`OrderNecessityGap = min_(pi in Pi_S) E_pi[sum_t delta*(h_t,pi(S_A(h_t)))]`.

This identity is the main structural interpretation of the metric.

## 4. Exact zero-gap characterization

`OrderNecessityGap = 0`

iff there exists a restricted policy `pi in Pi_S` that chooses only unrestricted-optimal actions on every history reachable under its own induced trajectory distribution.

A simple sufficient certificate is the implemented on-policy zero-conflict test:
- follow one deterministic tie-broken unrestricted-optimal policy;
- group reachable histories by `S_A`;
- if each reached class requests only one action, then a count-based policy reproduces that trajectory distribution exactly.

The tie-broken certificate is sufficient, not logically necessary: with action ties, two histories may have different selected actions while sharing another zero-regret action.

## 5. Global best-S_A solver

When on-policy conflicts exist, the code solves the best deterministic `S_A` policy globally with a mixed-integer linear program.

The optimization includes:
- reach probability of each history;
- history-action flow;
- one shared deterministic action variable per `S_A` class;
- true predictive observation probabilities;
- terminal posterior entropy objective.

For a finite acyclic horizon, deterministic restricted policies are sufficient for the optimum considered here.

## 6. Useful bounds

Because fixed open-loop sequences are a subset of `Pi_S`:

`OrderNecessityGap <= AdaptiveGap`

where:

`AdaptiveGap = IG_opt - IG_best-open-loop`.

For any explicit legal restricted policy `pi_c`:

`OrderNecessityGap <= IG_opt - IG(pi_c)`.

This makes cheap bypass policies useful as **upper-bound certificates**.

A sufficient positive lower-bound pattern is:

If every `Pi_S` policy must encounter a structural bottleneck with probability at least `m`, and the conditional common-action regret there is at least `rho`, then:

`OrderNecessityGap >= m*rho`.

The difficult part is proving non-bypassability: the lower bound must hold for every restricted route, not just the unrestricted-optimal route.

## 7. Prospective audit sequence

A practical order is:

1. **Open-loop upper bound**  
   If `AdaptiveGap < epsilon`, stop.

2. **Zero-regret representability**  
   If a restricted zero-regret policy exists, gap is zero.

3. **Cheap restricted candidates**  
   Try count projections, route changes, action-as-memory, robust fallback policies.

4. **Structural lower bound**  
   Establish an unavoidable regret bottleneck.

5. **Exact global solver**  
   Use MILP only when simpler arguments do not decide the case.

6. **Agent experiment**  
   Only after the environment itself has enough identified structural headroom.
