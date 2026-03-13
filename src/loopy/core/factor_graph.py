import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from itertools import product

@dataclass
class FactorGraph:
    """
    A simple factor graph for loopy BP experiments.
    Variables are binary (0/1).
    Factors are pairwise, stored as 2x2 numpy arrays.
    """
    n_vars: int
    edges: List[Tuple[int, int]]  # (var_i, var_j) pairs
    factors: Dict[Tuple[int, int], np.ndarray]  # edge -> 2x2 factor table

    def exact_marginals(self) -> np.ndarray:
        """
        Brute-force exact marginals over all 2^n assignments.
        Feasible for n <= 15 or so.
        """
        marginals = np.zeros(self.n_vars)
        Z = 0.0
        for assignment in product([0, 1], repeat=self.n_vars):
            w = 1.0
            for (i, j), f in self.factors.items():
                w *= f[assignment[i], assignment[j]]
            Z += w
            for v in range(self.n_vars):
                if assignment[v] == 1:
                    marginals[v] += w
        return marginals / Z