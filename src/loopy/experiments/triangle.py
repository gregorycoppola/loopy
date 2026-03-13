import numpy as np
from rich.console import Console
from rich.table import Table
from loopy.core.factor_graph import FactorGraph
from loopy.core.bp import run_loopy_bp
from loopy.core.metrics import kl_divergence, mae

console = Console()

def random_triangle(seed: int = None) -> FactorGraph:
    rng = np.random.default_rng(seed)
    factors = {
        (0, 1): rng.uniform(0.1, 1.0, (2, 2)),
        (1, 2): rng.uniform(0.1, 1.0, (2, 2)),
        (0, 2): rng.uniform(0.1, 1.0, (2, 2)),
    }
    return FactorGraph(
        n_vars=3,
        edges=[(0, 1), (1, 2), (0, 2)],
        factors=factors,
    )

def run(n_trials: int = 100):
    console.print("[bold cyan]Triangle Graph Experiment[/bold cyan]")
    console.print(f"Running {n_trials} trials with random factor tables.\n")

    results = []
    for seed in range(n_trials):
        g = random_triangle(seed=seed)
        exact = g.exact_marginals()
        bp_beliefs, n_iters, converged = run_loopy_bp(g)
        kl = kl_divergence(exact, bp_beliefs)
        error = mae(exact, bp_beliefs)
        results.append((converged, n_iters, kl, error))

    n_converged = sum(r[0] for r in results)
    avg_iters = np.mean([r[1] for r in results if r[0]])
    avg_kl = np.mean([r[2] for r in results if r[0]])
    avg_mae = np.mean([r[3] for r in results if r[0]])

    table = Table(title="Triangle Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Trials", str(n_trials))
    table.add_row("Converged", f"{n_converged}/{n_trials}")
    table.add_row("Avg iters (converged)", f"{avg_iters:.1f}")
    table.add_row("Avg KL divergence", f"{avg_kl:.6f}")
    table.add_row("Avg MAE", f"{avg_mae:.6f}")
    console.print(table)