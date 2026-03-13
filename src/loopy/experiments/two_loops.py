import numpy as np
from rich.console import Console
from rich.table import Table
from loopy.core.factor_graph import FactorGraph
from loopy.core.bp import run_loopy_bp
from loopy.core.metrics import kl_divergence, mae

console = Console()

def random_two_loops(seed: int = None) -> FactorGraph:
    """
    Two triangles sharing an edge: v0-v1-v2 and v1-v2-v3.
    Four variables, two loops, shared v1-v2 edge.

        v0
       /  \
      v1 - v2
       \  /
        v3
    """
    rng = np.random.default_rng(seed)
    factors = {
        (0, 1): rng.uniform(0.1, 1.0, (2, 2)),
        (0, 2): rng.uniform(0.1, 1.0, (2, 2)),
        (1, 2): rng.uniform(0.1, 1.0, (2, 2)),  # shared edge
        (1, 3): rng.uniform(0.1, 1.0, (2, 2)),
        (2, 3): rng.uniform(0.1, 1.0, (2, 2)),
    }
    return FactorGraph(
        n_vars=4,
        edges=[(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)],
        factors=factors,
    )

def run(n_trials: int = 100):
    console.print("[bold cyan]Two-Loop Graph Experiment[/bold cyan]")
    console.print("Two triangles sharing an edge (v1-v2). Four variables, two loops.\n")

    results = []
    for seed in range(n_trials):
        g = random_two_loops(seed=seed)
        exact = g.exact_marginals()
        bp_beliefs, n_iters, converged = run_loopy_bp(g)
        kl = kl_divergence(exact, bp_beliefs)
        error = mae(exact, bp_beliefs)
        results.append((converged, n_iters, kl, error))

    n_converged = sum(r[0] for r in results)
    avg_iters = np.mean([r[1] for r in results if r[0]])
    avg_kl = np.mean([r[2] for r in results if r[0]])
    avg_mae = np.mean([r[3] for r in results if r[0]])

    table = Table(title="Two-Loop Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Trials", str(n_trials))
    table.add_row("Converged", f"{n_converged}/{n_trials}")
    table.add_row("Avg iters (converged)", f"{avg_iters:.1f}")
    table.add_row("Avg KL divergence", f"{avg_kl:.6f}")
    table.add_row("Avg MAE", f"{avg_mae:.6f}")
    console.print(table)