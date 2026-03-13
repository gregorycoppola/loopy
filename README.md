# Loopy

Research into belief propagation on loopy factor graphs, and the
behavior of transformers implementing BP on non-tree structures.

## The Central Question

The paper *Transformers are Bayesian Networks* proves that a transformer
with BP weights computes exact marginal posteriors on tree-structured
factor graphs. The tree assumption is the one substantive limitation
of that result. This repo investigates what can be said about loopy
graphs.

The question splits into two parts:

1. **Convergence**: does iterative BP converge on the graphs we care about?
2. **Correctness**: when it converges, how close is the fixed point to
   the true posterior?

## What We Know

**Formally proved (in transformer-bp-lean):**
One forward pass of the transformer equals one round of BP, for any
factor graph — loopy or tree. The transformer implements BP exactly.
The limitation is not in the transformer, it is in what BP itself
guarantees on loopy graphs.

**Formally proved (in hard-bp-lean):**
On trees, BP converges in exactly `diameter(T)` rounds to the exact
marginal posteriors. This is Pearl (1988), formalized in Lean 4.

**Not yet proved:**
Convergence and posterior correctness on loopy graphs. When loopy BP
converges, its fixed point minimizes the Bethe free energy (Yedidia
et al. 2003), which approximates but does not in general equal the
true posterior.

**Empirically established (Paper 1, coppola2024):**
The dating graph — `lonely(jack)` and `exciting(jill)` feeding into
`like(jack, jill)` via disjunction, with `like(jack, jill)` and
`like(jill, xjack)` feeding into `date(jack, jill)` via conjunction
— is a loopy structure. Iterative BP was run on this graph and
converged to correct posteriors across all tested configurations.
This is direct evidence that the transformer implementing BP faithfully
would exhibit the same behavior.

**From the literature:**
Loopy BP has been found to converge empirically across a wide range
of graph structures (Murphy et al. 1999, Smith and Eisner 2008).
On graphs with weak loops or small treewidth the Bethe approximation
is often tight. Conditions under which loopy BP is exact are known
for certain graph classes and potential functions but a general theory
is open.

## The Strongest Claim We Can Make Now

The transformer with BP weights implements belief propagation on any
factor graph. On trees, the result is provably exact. On loopy graphs,
the transformer inherits BP's empirical track record — which is strong
— without a theoretical exactness guarantee. For QBBN graphs arising
from grounded natural language knowledge bases, the loop structure is
constrained by the grammar and the grounding, which may be exploitable
for tighter guarantees.

## Structure of This Repo