# The Dating Graph: A Loopy Case Study

## The Graph Structure

The dating graph from Paper 1 (Coppola 2024) is the canonical
empirical example of loopy BP in the QBBN setting. The structure is:

    lonely(jack) ----\
                      OR ----> like(jack, jill) ---\
    exciting(jill) --/                              AND --> date(jack, jill)
                                                   /
    like(jill, jack) --------------------------/

This graph contains a loop. The and-or alternating structure of the
QBBN creates bipartite loops that are not trees in general.

## Why It Is Loopy

In the QBBN, the universal rule:

    always [x:jack, y:jill]: like(x,y) AND like(y,x) -> date(x,y)

grounds to a conjunction factor connecting `like(jack, jill)`,
`like(jill, jack)`, and `date(jack, jill)`. The two `like` nodes
each also have their own parents (`lonely`, `exciting`). When
multiple jack/jill pairs are grounded simultaneously and share
factor nodes, cycles appear.

## What Paper 1 Found

Iterative BP was run on this graph across multiple experimental
conditions:

- **No evidence**: prior probabilities stable across iterations,
  matching closed-form calculations.
- **Forward only**: observing `like(jill, jack) = true` propagated
  correctly to `date(jack, jill)` without affecting independent nodes.
- **Forward and backward**: observing `like(jack, jill) = true`
  propagated both to children and back to parents correctly.
- **Backward only**: observing `date(jack, jill) = true` propagated
  backward through the AND gate to both `like` nodes and their
  ancestors.

In all cases, iterative BP converged. The posteriors matched
by-hand calculations (with small noise from the SGD estimate
of the weights).

## What This Means for the Transformer

The transformer with BP weights would reproduce these results
exactly. One forward pass of the transformer equals one round
of iterative BP. Running the transformer for k steps on the
dating graph is exactly k rounds of iterative BP on the dating
graph. The empirical convergence of Paper 1 is therefore direct
evidence that the transformer converges on this loopy structure.

## The Open Questions

1. Does convergence hold across all factor table entries, not
   just the learned ones?
2. How many iterations are needed as the graph scales?
3. How close are the Bethe marginals to the true posteriors
   on this specific graph class?

These are the natural first experiments for this repo.