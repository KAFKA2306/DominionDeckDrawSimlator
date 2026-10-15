# Lean 4 proof pilot

This directory introduces machine-checked proofs for the simplified Dominion draw model.
Toolchain: `leanprover/lean4:v4.29.0` (pinned).

## Proof coverage

- An empty deck finishes successfully.
- Processing a nonempty deck with zero available actions stops.
- Every deck with at least as many initial actions as cards finishes,
  independent of card order and individual draw counts.
- Therefore every deck of size at most five finishes when the initial hand is five.

These properties support the `deckSize <= initialHandSize` early return
in `probability.js`, assuming the JavaScript implementation follows the
model encoded in `DrawModel.lean`.

## Not yet proven

- Equality between the JavaScript implementation and the Lean model.
- Correctness of the weighted recursive probability formula or memoization.
- The pseudo-random generator, Monte Carlo confidence intervals, URL parsing
  or DOM behavior.
- Runtime integration, supply-chain security, or deployment.

Do not delete the existing Node tests, Gitleaks checks, or GitHub Actions:
Lean proofs must themselves be executed in CI, and the unproven boundaries
still require tests.

To check locally (Lean installed):

```sh
cd proofs
lake build
```

The repository's `Lean 4 formal proofs` workflow checks this on pull requests
that touch `proofs/**` and on relevant pushes to `main`.
