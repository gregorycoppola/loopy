# The Strongest Claims We Can Make Now

## Fully Proved

1. A transformer with BP weights implements one round of BP on
   any factor graph — loopy or tree. (transformer-bp-lean)

2. On trees, iterated BP converges in diameter(T) rounds to the
   exact marginal posteriors. (hard-bp-lean, Pearl 1988)

3. Therefore: a transformer with BP weights on a tree-structured
   QBBN computes exact posteriors. No empirical assumptions.

4. The transformer token encoding uses exactly 2n^2 routing
   classes, a logical necessity not a design choice. (godel)

## Empirically Established

5. Gradient descent independently recovers BP weights on
   two-variable factor graphs to three decimal places with no
   construction hints. (bayes-learner)

6. Loopy BP converges on the dating graph across all tested
   evidence conditions, with posteriors matching closed-form
   calculations. (Paper 1)

## What Follows From 1 + 6

The transformer with BP weights converges on the dating graph,
because it implements exactly the BP that Paper 1 showed
converges. The convergence is not separately proved for the
transformer — it follows directly from the implementation
theorem and the empirical BP result.

## The Gap

What is not proved: that loopy BP converges on QBBN graphs
in general, or that when it converges its fixed point is close
to the true posterior.

What is empirically plausible: that for QBBN graphs arising
from typical grounded knowledge bases, loopy BP behaves well
because the loop structure is sparse and long.

## The Honest Summary for Paper Submission

The no-hallucination theorem holds exactly on trees. On loopy
graphs, the transformer implements BP, and BP's empirical track
record is strong — including on the specific loopy QBBN
structure tested in Paper 1. A theoretical exactness guarantee
for loopy graphs is the primary open problem and the natural
next direction for this research program.