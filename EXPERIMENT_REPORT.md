
# Experiment Report: Loopy Belief Propagation on QBBN-Structured Graphs

## Background

The paper *Transformers are Bayesian Networks* (Coppola 2026) proves that a transformer
with BP weights implements exact Bayesian inference on tree-structured factor graphs. The
tree assumption is the one substantive limitation of that result. On a loopy graph, the
transformer still implements BP exactly — one forward pass still equals one round of belief
propagation — but BP itself carries no convergence guarantee and no exactness guarantee on
loopy graphs. When loopy BP does converge, its fixed point minimizes the Bethe free energy
(Yedidia, Freeman, Weiss 2003), which approximates but does not in general equal the true
posterior.

The question this experiment addresses: is the tree limitation a practical problem for the
graph structures that arise in the QBBN setting?

## Hypothesis

Loopy BP converges reliably on QBBN-structured factor graphs, and the Bethe approximation
is tight — meaning the fixed point is close to the true posterior even though exactness is
not guaranteed.

## Motivation for the Hypothesis

Three sources of prior evidence motivated this hypothesis before any experiment was run.

First, the literature on loopy BP is broadly positive. Murphy, Weiss, and Jordan (1999)
conducted an empirical study across a wide range of graph structures and found convergence
to be the norm rather than the exception. Smith and Eisner (2008) found loopy BP effective
for dependency parsing — a structured NLP task directly analogous to QBBN inference.
The theoretical failure cases involve dense graphs with strong frustrated potentials, which
are not characteristic of grounded natural language knowledge bases.

Second, QBBN graphs have structural properties that place them in the regime where loopy
BP is known to work well. Loops arise only when the same entity appears in multiple rules,
or when the conclusion of one rule is the premise of another. In typical knowledge bases
this is sparse. The resulting loops are long and the potentials are moderate — exactly the
conditions under which the Bethe approximation is known to be tight.

Third, Paper 1 (Coppola 2024) ran iterative BP on the dating graph — a loopy QBBN
structure — and found empirical convergence to correct posteriors across all tested evidence
conditions. That was a single graph with specific structure; the question was whether it
generalized.

## Experimental Design

We implemented a common framework for loopy BP experiments: a factor graph representation,
an iterative BP solver with convergence detection, and brute-force exact marginal computation
(feasible for graphs up to approximately 15 variables). For each experiment we generated 100
random factor graphs of the target structure, with factor table entries drawn uniformly from
[0.1, 1.0]. For each trial we measured three quantities: whether BP converged (within 100
iterations, tolerance 1e-6), the number of iterations until convergence, and the KL
divergence and MAE between the BP marginals and the brute-force exact marginals.

Five graph structures were tested, chosen to span a range of complexity and structural
relevance to the QBBN:

- **Triangle**: three variables, one loop. The simplest possible loopy factor graph.
- **Square**: four variables arranged in a cycle, one loop. Longer loop than the triangle.
- **Dating graph**: five variables, one loop. The canonical QBBN example from Paper 1,
  with OR and AND factors reflecting the structure of grounded natural language rules.
- **Two loops**: four variables, two loops (two triangles sharing an edge). The simplest
  multi-loop structure, testing whether convergence holds when loops interact.
- **QBBN chain**: six variables, one loop. Two grounded rules sharing an entity, with
  a feedback edge closing the loop — the simplest realistic QBBN loop arising from
  natural language grounding.

## Results

| Experiment   | Vars | Loops | Converged | Avg iters | Avg KL   | Avg MAE  |
|--------------|------|-------|-----------|-----------|----------|----------|
| Triangle     | 3    | 1     | 100/100   | 8.5       | 0.000045 | 0.002091 |
| Square       | 4    | 1     | 100/100   | 8.4       | 0.000002 | 0.000382 |
| Dating graph | 5    | 1     | 100/100   | 13.2      | 0.000102 | 0.003590 |
| Two loops    | 4    | 2     | 100/100   | 10.2      | 0.000086 | 0.003111 |
| QBBN chain   | 6    | 1     | 100/100   | 8.7       | 0.000021 | 0.001055 |

500 trials total. 500 convergences. Convergence rate: 100%.

## Conclusions

**Convergence.** Loopy BP converged on every trial across all five graph structures. This
includes the two-loop graph, where interacting loops might have been expected to cause
oscillation. Convergence was not fragile — it held across 100 randomly drawn factor tables
per structure, not just carefully chosen ones.

**Approximation quality.** The Bethe approximation was extremely tight in all cases. The
worst mean KL divergence across all five experiments was 0.000102 (dating graph). The best
was 0.000002 (square). These are not approximation errors that would materially affect any
downstream inference task. The Bethe fixed point is, for practical purposes, the exact
posterior on these graph structures.

**Iteration count.** Convergence was fast. The most complex structure (dating graph, 5
variables, structured OR/AND potentials) required an average of 13.2 iterations. All others
converged in under 11 iterations on average. This is consistent with the theoretical
expectation that convergence rate depends on loop length and coupling strength, both of
which are moderate in QBBN-structured graphs.

**Scope of the conclusion.** These results are empirical, not theoretical. They establish
that on the graph structures tested — single-loop and two-loop graphs with up to six
variables and random factor tables — loopy BP behaves as well in practice as exact BP does
on trees. They do not prove convergence in general. The theoretical failure cases for loopy
BP (dense graphs, many short loops, strong frustrated potentials) are not represented here,
because they are not representative of the graphs that arise from grounding natural language
knowledge bases.

**Implication for the paper.** The tree assumption in the no-hallucination theorem is a
limitation on the theoretical guarantee, not on the empirical behavior of the system on the
graph structures that arise in practice. For QBBN graphs arising from grounded natural
language rules, loopy BP converges reliably and the Bethe approximation is tight. The
transformer with BP weights inherits this empirical track record. A theoretical convergence
guarantee for loopy QBBN graphs remains the primary open problem and the natural next
direction for this research program.