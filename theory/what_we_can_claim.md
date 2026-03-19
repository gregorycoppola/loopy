# What We Can Claim

A precise account of what is established, what is
conjectured, and what is unknown about loopy BP in
the context of the Transformers are Bayesian Networks
framework.

## Formally Proved

**The transformer implements BP on any graph.**
One forward pass of a sigmoid transformer equals one
round of weighted loopy BP on the implicit factor
graph G(W), for any weights W and any graph structure
— loopy or tree. Proved in transformer-bp-lean.

**BP is exact on trees.**
On a tree-structured factor graph, BP converges in
exactly diameter(T) rounds to the exact marginal
posteriors. Proved in hard-bp-lean. This is Pearl
(1988) formalized in Lean 4.

**Loopy BP fixed points minimize Bethe free energy.**
When loopy BP converges on a loopy graph, the fixed
point minimizes the Bethe free energy — a variational
approximation to the true log partition function.
This is Yedidia et al. (2003). Not formalized in
Lean but established in the literature.

## Empirically Established

**Loopy BP converges on QBBN-structured graphs.**
500 trials across five graph structures (triangle,
square, dating graph, two loops, QBBN chain). All
500 converged. Worst mean KL divergence 0.000102.
See EXPERIMENT_REPORT.md.

**Gradient descent finds BP weights on tree graphs.**
The bayes-learner experiment trained a transformer
on a two-variable tree factor graph and found weights
converging to near-pure BP (val MAE 0.000752).
Consistent with the uniqueness theorem.

## Conjectured

**Backprop learns loop-compensating weights.**
When trained on loopy data, backprop finds weights
that deviate from pure BP weights in a way that
compensates for loop correlations — downweighting
positively correlated evidence sources, upweighting
negatively correlated ones. The learned weights
implement a form of variational inference that
makes the Bethe approximation tighter than pure
BP weights would. See theory/learned_weights_and_loops.md.

**Loop structure of grounded QBBN graphs is exploitable.**
For QBBN graphs arising from grounded natural language
knowledge bases, loops arise only when the same entity
appears in multiple rules or when rule conclusions
are premises elsewhere. This constrained loop structure
may allow tighter convergence and correctness guarantees
than general loopy graphs. Not yet formalized.

**Hybrid factor graphs extend the results.**
The boolean framework covers discrete propositional
reasoning. Production transformers also implement BP
on continuous-valued nodes — the function vector heads
in the mechanistic interpretability literature are
doing weighted aggregation over real-valued quantities.
The hybrid extension is theoretically consistent with
all existing results and resolves the apparent gap
for diffuse attention heads. See interp repo conclusions.

## Unknown

**Convergence guarantees for loopy QBBN graphs.**
The empirical results show convergence on small QBBN
graphs. Whether convergence is guaranteed for larger
QBBN graphs with more complex loop structure is not
known. The loop structure constraints of grounded
QBBN graphs may be exploitable for a convergence
theorem but this has not been pursued.

**The no-hallucination corollary for loopy graphs.**
On trees the corollary is exact — BP weights give
exact posteriors. On loopy graphs with learned
compensating weights, what correctness guarantee
is available? Can you bound the hallucination rate
as a function of the loop structure and the quality
of the Bethe approximation?

**The no-hallucination corollary for continuous nodes.**
The hybrid extension introduces continuous-valued
nodes. What does exact inference mean for a continuous
node? What is the analog of the no-hallucination
corollary for a hybrid boolean/continuous factor graph?

**Whether backprop finds loop-compensating weights.**
The conjecture in theory/learned_weights_and_loops.md
is not proved. The bayes-learner result on trees is
consistent with it but does not confirm it. Direct
experiments on loopy graphs with known correlation
structure would test it. See experiments/plan.md.