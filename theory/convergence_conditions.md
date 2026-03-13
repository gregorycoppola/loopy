# Convergence Conditions for Loopy BP

## The Basic Facts

Loopy BP is not guaranteed to converge in general. When it does
not converge, it oscillates between states without settling. When
it does converge, the fixed point minimizes the Bethe free energy,
which is an approximation to the true posterior.

On trees, both problems disappear: BP always converges in
diameter(T) rounds, and the fixed point is the exact posterior.

## Known Sufficient Conditions for Convergence

**Diagonal dominance (Mooij and Kappen 2007)**
BP converges if the factor potentials satisfy a diagonal dominance
condition: informally, if each variable's self-potential dominates
its interactions with neighbors.

**Contractivity (Tatikonda and Jordan 2002)**
BP converges if the message update operator is contractive in an
appropriate norm. This gives convergence rate as well as
convergence itself.

**Walk-summability (Malioutov et al. 2006)**
For Gaussian models, BP converges if and only if the model is
walk-summable. This gives a complete characterization in the
Gaussian case.

**Small spectral radius (Ihler et al. 2005)**
If the spectral radius of a certain matrix derived from the
factor graph is less than 1, BP converges.

## Known Conditions for Exactness at Fixed Point

**Trees**: exact always. The fundamental result.

**Graphs with one loop**: correction factors are known
analytically (Montanari and Rizzo 2005).

**Gaussian models**: BP is always exact for jointly Gaussian
distributions regardless of graph structure.

## The QBBN Case

QBBN factor graphs have specific structure that may be exploitable:

- The graph is bipartite (variable nodes and factor nodes alternate)
- Factor potentials are either deterministic (AND gates) or
  sigmoid (OR gates with learned weights)
- The graph arises from grounding a finite set of universally
  quantified rules over a finite domain
- Loop structure is determined by the rule structure and the
  domain size

The key observation: loops in a QBBN graph arise when the same
entity appears in multiple rules, or when a conclusion of one
rule is a premise of another. For typical natural language
knowledge bases, these loops are sparse and long — which is
exactly the regime where loopy BP is known to work well
empirically.

## Conjectures Worth Investigating

**Conjecture 1**: For QBBN graphs arising from grounded natural
language knowledge bases with typical rule structures, loopy BP
converges with high probability over randomly drawn factor table
entries.

**Conjecture 2**: For QBBN graphs with loop length greater than
some threshold L, the Bethe marginals are within epsilon of the
true posteriors, where epsilon depends on the strength of the
loop potentials.

**Conjecture 3**: The transformer with BP weights on a QBBN graph
converges in practice in O(diameter) steps even on loopy graphs,
because the effective influence of loops decays exponentially
with loop length.