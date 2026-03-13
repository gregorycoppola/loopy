# Experiment Plan

## Starting Point

The bayes-learner repo has the infrastructure:
- Factor graph generation
- Token encoding
- Transformer training and evaluation
- Comparison against exact closed-form posteriors

The two-variable graph used in bayes-learner is a tree. We need
to extend to loopy graphs.

## Experiment 1: Simplest Loopy Graph

The simplest loopy factor graph: a triangle.

    v0 --- f01 --- v1
     \              |
      f02          f12
        \            |
         v2 --------/

Three variable nodes, three factor nodes, one loop.

Questions:
- Does BP converge on this graph for random factor tables?
- How many iterations until convergence?
- How close are the BP marginals to the true posteriors
  (computable by brute force over 2^3 = 8 assignments)?
- Does the transformer trained on this graph match BP?

## Experiment 2: The Dating Graph

Implement the dating graph from Paper 1 in the bayes-learner
framework:

- Variables: lonely(jack), exciting(jill), like(jack,jill),
  like(jill,jack), date(jack,jill)
- Factors: OR for like(jack,jill), independent prior for
  like(jill,jack), AND for date(jack,jill)

Questions:
- Reproduce Paper 1 results in the new framework
- Measure convergence rate as a function of factor table entries
- Compare Bethe marginals to exact marginals (brute force over
  2^5 = 32 assignments)

## Experiment 3: Systematic Loop Structure Variation

Generate random factor graphs varying:
- Loop length (3, 4, 5, 6, ...)
- Loop strength (weak vs strong potentials)
- Number of loops

For each, measure:
- Convergence rate and whether BP converges
- KL divergence between Bethe marginals and true posteriors
- Whether the transformer trained on these graphs matches BP

## Experiment 4: Scaling

Take the strongest positive result from experiments 1-3 and
scale up to larger graphs, more variables, denser loop structure.

Goal: characterize empirically the regime where the transformer
with BP weights gives reliable approximate inference, and where
it breaks down.

## What a Strong Positive Result Would Look Like

For QBBN-structured graphs (bipartite, alternating AND/OR,
arising from grounded rules), loopy BP converges reliably
and the Bethe approximation is tight (KL divergence small)
for the graph structures that arise naturally from grounded
language knowledge bases.