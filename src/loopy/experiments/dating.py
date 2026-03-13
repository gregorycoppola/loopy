import numpy as np
from rich.console import Console
from rich.table import Table
from loopy.core.factor_graph import FactorGraph
from loopy.core.bp import run_loopy_bp
from loopy.core.metrics import kl_divergence, mae

console = Console()

def dating_graph(seed: int = None) -> FactorGraph:
    """
    The dating graph from Paper 1 (Coppola 2024).

    Variables:
        0: lonely(jack)
        1: exciting(jill)
        2: like(jack, jill)
        3: like(jill, jack)
        4: date(jack, jill)

    Factors:
        (0,2), (1,2): OR gate — like(jack,jill) from lonely(jack) + exciting(jill)
        (3,4), (2,4): AND gate — date from like(jack,jill) + like(jill,jack)
        (3,):         independent prior on like(jill,jack)

    Loop: 2 -> 4 <- 3, and 3 has no shared parents with 2,
    but 2 and 3 both feed into 4, creating the loop through
    the AND factor.
    """
    rng = np.random.default_rng(seed)

    # OR factor: like(jack,jill) | lonely(jack), exciting(jill)
    # P(like=1 | lonely, exciting) ~ sigmoid(w * phi)
    # Approximate as noisy-OR with weight drawn randomly
    w = rng.uniform(0.5, 2.0)
    def or_factor():
        f = np.zeros((2, 2))
        for a in range(2):
            for b in range(2):
                p = 1 - (1 - 0.05) * (1 - a * 0.9) * (1 - b * 0.9)
                f[a, b] = p if rng.random() > 0.5 else 1 - p
        return np.abs(rng.uniform(0.1, 1.0, (2, 2)))

    # AND factor: date | like(jack,jill), like(jill,jack)
    def and_factor():
        f = np.zeros((2, 2))
        f[0, 0] = rng.uniform(0.7, 1.0)  # both false -> date unlikely
        f[0, 1] = rng.uniform(0.1, 0.3)
        f[1, 0] = rng.uniform(0.1, 0.3)
        f[1, 1] = rng.uniform(0.7, 1.0)  # both true -> date likely
        return f

    factors = {
        (0, 2): np.abs(rng.uniform(0.1, 1.0, (2, 2))),  # lonely -> like(j,j)
        (1, 2): np.abs(rng.uniform(0.1, 1.0, (2, 2))),  # exciting -> like(j,j)
        (2, 4): and_factor(),                             # like(j,j) -> date
        (3, 4): and_factor(),                             # like(jill,jack) -> date
        (3, 1): np.abs(rng.uniform(0.1, 1.0, (2, 2))),  # weak coupling closing loop
    }
    return FactorGraph(
        n_vars=5,
        edges=[(0, 2), (1, 2), (2, 4), (3, 4), (3, 1)],
        factors=factors,
    )

def run(n_trials: int = 100):
    console.print("[bold cyan]Dating Graph Experiment[/bold cyan]")
    console.print(f"Running {n_trials} trials with random factor tables.\n")

    results = []
    for seed in range(n_trials):
        g = dating_graph(seed=seed)
        exact = g.exact_marginals()
        bp_beliefs, n_iters, converged = run_loopy_bp(g)
        kl = kl_divergence(exact, bp_beliefs)
        error = mae(exact, bp_beliefs)
        results.append((converged, n_iters, kl, error))

    n_converged = sum(r[0] for r in results)
    avg_iters = np.mean([r[1] for r in results if r[0]])
    avg_kl = np.mean([r[2] for r in results if r[0]])
    avg_mae = np.mean([r[3] for r in results if r[0]])

    table = Table(title="Dating Graph Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Trials", str(n_trials))
    table.add_row("Converged", f"{n_converged}/{n_trials}")
    table.add_row("Avg iters (converged)", f"{avg_iters:.1f}")
    table.add_row("Avg KL divergence", f"{avg_kl:.6f}")
    table.add_row("Avg MAE", f"{avg_mae:.6f}")
    console.print(table)