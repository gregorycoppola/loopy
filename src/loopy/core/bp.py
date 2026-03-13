import numpy as np
from loopy.core.factor_graph import FactorGraph
from typing import Dict, Tuple

def run_loopy_bp(
    graph: FactorGraph,
    max_iters: int = 100,
    tol: float = 1e-6,
    damping: float = 0.0,
) -> Tuple[np.ndarray, int, bool]:
    msgs: Dict[Tuple[int, int], np.ndarray] = {}
    for (i, j) in graph.edges:
        msgs[(i, j)] = np.array([0.5, 0.5])
        msgs[(j, i)] = np.array([0.5, 0.5])

    def neighbors(v):
        return [j for (i, j) in graph.edges if i == v] + \
               [i for (i, j) in graph.edges if j == v]

    def factor(i, j):
        if (i, j) in graph.factors:
            return graph.factors[(i, j)]
        elif (j, i) in graph.factors:
            return graph.factors[(j, i)].T
        else:
            raise KeyError(f"No factor found for edge ({i}, {j})")

    for iteration in range(max_iters):
        new_msgs = {}
        for (i, j) in list(msgs.keys()):
            f = factor(i, j)
            incoming = np.ones(2)
            for k in neighbors(i):
                if k != j:
                    incoming *= msgs[(k, i)]
            msg = np.array([
                np.sum(f[:, xj] * incoming) for xj in [0, 1]
            ], dtype=float)
            msg /= msg.sum()
            if damping > 0.0:
                msg = (1 - damping) * msg + damping * msgs[(i, j)]
            new_msgs[(i, j)] = msg

        delta = max(
            np.max(np.abs(new_msgs[k] - msgs[k])) for k in msgs
        )
        msgs = new_msgs
        if delta < tol:
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