import numpy as np
from loopy.core.factor_graph import FactorGraph
from typing import Dict, Tuple

def run_loopy_bp(
    graph: FactorGraph,
    max_iters: int = 100,
    tol: float = 1e-6,
    damping: float = 0.0,
) -> Tuple[np.ndarray, int, bool]:
    """
    Run loopy belief propagation on a factor graph.
    Returns (marginals, n_iters, converged).
    Messages are stored as msg[i][j] = message from var i to var j.
    """
    # Initialize all messages to 0.5
    msgs: Dict[Tuple[int, int], np.ndarray] = {}
    for (i, j) in graph.edges:
        msgs[(i, j)] = np.array([0.5, 0.5])
        msgs[(j, i)] = np.array([0.5, 0.5])

    def neighbors(v):
        return [j for (i, j) in graph.edges if i == v] + \
               [i for (i, j) in graph.edges if j == v]

    def factor(i, j):
        return graph.factors.get((i, j), graph.factors.get((j, i)).T)

    for iteration in range(max_iters):
        new_msgs = {}
        for (i, j) in list(msgs.keys()):
            f = factor(i, j)
            # Product of incoming messages to i except from j
            incoming = np.ones(2)
            for k in neighbors(i):
                if k != j:
                    incoming *= msgs[(k, i)]
            # Message i -> j: sum over x_i of f(x_i, x_j) * incoming(x_i)
            msg = np.array([
                np.sum(f[:, xj] * incoming) for xj in [0, 1]
            ], dtype=float)
            msg /= msg.sum()
            # Damping
            if damping > 0.0:
                msg = (1 - damping) * msg + damping * msgs[(i, j)]
            new_msgs[(i, j)] = msg

        # Check convergence
        delta = max(
            np.max(np.abs(new_msgs[k] - msgs[k])) for k in msgs
        )
        msgs = new_msgs
        if delta < tol:
            # Compute beliefs
            beliefs = _compute_beliefs(graph, msgs, neighbors)
            return beliefs, iteration + 1, True

    beliefs = _compute_beliefs(graph, msgs, neighbors)
    return beliefs, max_iters, False


def _compute_beliefs(graph, msgs, neighbors_fn):
    beliefs = np.zeros(graph.n_vars)
    for v in range(graph.n_vars):
        b = np.ones(2)
        for k in neighbors_fn(v):
            b *= msgs[(k, v)]
        b /= b.sum()
        beliefs[v] = b[1]
    return beliefs