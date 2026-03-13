import numpy as np

def kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-10) -> float:
    """
    KL divergence D(p || q) for arrays of Bernoulli marginals.
    Averages KL over all variables.
    """
    total = 0.0
    for pi, qi in zip(p, q):
        # Bernoulli KL
        p_dist = np.array([1 - pi, pi]) + eps
        q_dist = np.array([1 - qi, qi]) + eps
        p_dist /= p_dist.sum()
        q_dist /= q_dist.sum()
        total += np.sum(p_dist * np.log(p_dist / q_dist))
    return total / len(p)

def mae(p: np.ndarray, q: np.ndarray) -> float:
    return float(np.mean(np.abs(p - q)))