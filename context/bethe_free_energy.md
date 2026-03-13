# Bethe Free Energy and Loopy BP

## What the Bethe Free Energy Is

When loopy BP converges, its fixed point can be characterized
variationally: it minimizes the Bethe free energy, which is an
approximation to the true variational free energy of the distribution.

The true free energy is:

    F(b) = sum_i H(b_i) - sum_ij I(b_i, b_j)

where `H` is entropy and `I` is mutual information. The Bethe
approximation replaces the true entropy with a sum of local entropies
over nodes and factors, ignoring long-range correlations induced by
loops.

On a tree, the Bethe free energy equals the true free energy exactly.
This is why BP is exact on trees: the fixed point of the variational
problem is the true posterior.

On a loopy graph, the Bethe approximation introduces error. The size
of the error depends on the strength of the correlations induced by
the loops. Weak loops (long, with weak potentials) contribute little
error. Strong short loops with strong potentials can produce large
errors.

## When Loopy BP is Known to Be Exact

Several conditions are known under which loopy BP gives exact
marginals despite loops:

1. **Gaussian graphical models**: loopy BP is exact for Gaussian
   distributions on any graph structure.

2. **Graphs with a single loop**: for graphs with exactly one loop,
   the Bethe approximation can be corrected analytically.

3. **Attractive binary models at high temperature**: when potentials
   are weak, perturbative corrections to Bethe are small.

4. **Graphs with small treewidth**: junction tree algorithms give
   exact inference in time exponential in treewidth; for small
   treewidth the exact answer is tractable.

5. **Certain symmetric models**: models with specific symmetry
   properties can give exact Bethe marginals.

## The Key References

- Yedidia, Freeman, Weiss (2003): the foundational paper connecting
  loopy BP to Bethe free energy minimization.
- Murphy, Weiss, Jordan (1999): empirical study showing loopy BP
  converges and gives good approximations on a range of graphs.
- Wainwright and Jordan (2008): variational inference perspective,
  relating Bethe to a broader family of approximations.

## Implications for the Transformer

The transformer with BP weights does exactly what BP does. On loopy
graphs this means:

- If BP converges, the transformer converges to the same fixed point
- That fixed point minimizes the Bethe free energy
- The quality of the approximation depends on the loop structure
  and potential strengths of the specific factor graph

The transformer does not introduce additional approximation error
beyond what BP itself introduces. The question of posterior quality
is purely a question about BP on the graph in question.