# Backprop and the Independence Assumption

## The Independence Assumption in BP

The log-odds algebra underlying belief propagation is exact
under one condition: the evidence sources arriving at a node
are independent given that node's value.

    logit(P(H | e0, e1)) = logit(m0) + logit(m1)

This equality holds exactly when e0 and e1 are independent
given H. On a tree-structured factor graph this holds by
construction — messages arriving at any node come from
disjoint subtrees that share no variables. Independence
is guaranteed by the graph structure.

On a loopy graph it fails. The same variable can influence
a node through multiple paths. The messages arriving at a
node are correlated — they carry overlapping information
about the same upstream variables. Adding their log-odds
double-counts that shared information and produces
overconfident beliefs.

This is why BP is exact on trees and approximate on loops.
Not because the algorithm is different — the same algorithm
runs in both cases. Because the independence assumption
is satisfied on trees and violated on loops.

## What Backprop Does

When a transformer is trained by backprop on next-token
prediction, the gradients push the weights toward
configurations that minimize prediction error on the
actual data distribution. The data distribution reflects
the true correlation structure of the world — variables
that are correlated in reality are correlated in the
training data.

If the implicit factor graph is loopy — which it is for
any language model trained on natural text — then the
pure BP weights (w0 = w1 = 1, b = 0 in the FFN) are
not optimal. They assume independence where the data
has correlations. The prediction error on correlated
data would be suboptimal with pure BP weights.

Backprop corrects for this. If two evidence sources e0
and e1 are positively correlated — they tend to fire
together because they share a common cause — then pure
BP overcounts their combined evidence. Backprop learns
to downweight each source relative to what independent
BP would assign, implicitly compensating for the
positive correlation.

If two evidence sources are negatively correlated —
one tends to fire when the other does not — backprop
learns to upweight each one, compensating for the
mutual exclusion.

The learned weights are not the pure BP weights. They
are the weights that minimize prediction error on the
actual correlated data distribution. This is a richer
and more powerful configuration than pure BP weights.

## The Bethe Free Energy Connection

When loopy BP converges, its fixed point minimizes the
Bethe free energy — a variational approximation to the
true log partition function. The Bethe approximation
accounts for some but not all of the correlation
structure in a loopy graph. It is exact on trees and
approximate on loopy graphs, with the approximation
quality depending on the loop structure.

Backprop trained on real data goes further than the
Bethe approximation. It minimizes prediction error on
the true data distribution, which implicitly accounts
for all correlations in the data — not just the ones
the Bethe approximation captures.

The relationship between the weights backprop finds
and the Bethe free energy fixed points is not yet
formally characterized. This is the open conjecture
in theory/learned_weights_and_loops.md.

## Why This Matters for the Theory

The shannon paper proves: a transformer with pure BP
weights implements exact BP on the implicit factor
graph. The uniqueness theorem says: exact posteriors
force pure BP weights.

But trained transformers do not have pure BP weights
unless trained explicitly to do so (as in bayes-learner).
They have weights optimized for prediction error on
a correlated data distribution. These weights implement
weighted BP with non-unit weights — the general Ψor
function with w0 ≠ w1 and b ≠ 0.

The general theorem covers this case: any weights
implement weighted loopy BP on the implicit factor
graph. But the factor potentials encoded by the
learned weights are not the true conditional
probabilities of the declared knowledge base —
they are adjusted versions that compensate for
the loop correlations in the data.

This is not a failure of the theory. It is the theory
working correctly for a loopy graph. The learned weights
are the model's best approximation to the true factor
potentials given the loop structure it is working with.

## The Empirical Prediction

If backprop de-correlates the weights to compensate
for loop correlations, then:

Models trained on data with stronger correlations
should learn weights that deviate more from pure BP
weights. Models trained on data with weaker correlations
(more tree-like dependency structure) should learn
weights closer to pure BP weights.

The bayes-learner experiment trained on a two-variable
factor graph — the simplest possible structure, no
loops — and found weights very close to pure BP weights
(val MAE 0.000752). This is consistent: no loops, no
correlation to compensate for, weights converge to
pure BP.

A model trained on a loopy graph with strong correlations
should show systematic deviation from pure BP weights
in the FFN, with the deviation pattern reflecting the
correlation structure of the loops.

This is testable. See experiments/plan.md for proposed
experiments.