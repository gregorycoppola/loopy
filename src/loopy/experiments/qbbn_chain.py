import numpy as np
from rich.console import Console
from rich.table import Table
from loopy.core.factor_graph import FactorGraph
from loopy.core.bp import run_loopy_bp
from loopy.core.metrics import kl_divergence, mae

console = Console()

def qbbn_chain_graph(seed: int = None) -> FactorGraph:
    """
    Two grounded QBBN rules sharing an entity, creating a loop.

    Variables:
        0: popular(jack)
        1: lonely(jack)       -- shared entity creates the loop
        2: like(jack, jill)
        3: like(jack, bob)
        4: date(jack, jill)
        5: date(jack, bob)

    Rules:
        popular(jack) -> like(jack, jill)   [OR factor]
        popular(jack) -> like(jack, bob)    [OR factor]
        lonely(jack)  -> like(jack, jill)   [OR factor, shared conclusion]
        like(jack, jill) -> date(jack, jill) [OR factor]
        like(jack, bob)  -> date(jack, bob)  [OR factor]
        date(jack, jill) -> lonely(jack)     [feedback: loop closing edge]

    Loop: popular(jack) -> like(jack,jill) -> date(jack,jill) -> lonely(jack)
          -> like(jack,jill) [cycle through shared entity jack]
    """
    rng = np.random.default_rng(seed)

    def or_factor(rng):
        # Noisy OR-style: factor table with higher weight when input=1
        f = rng.uniform(0.1, 1.0, (2, 2))
        f[1, :] *= rng.uniform(1.5, 3.0)  # stronger signal when parent is true
        return np.clip(f, 0.05, 5.0)

    factors = {
        (0, 2): or_factor(rng),   # popular -> like(jack,jill)
        (0, 3): or_factor(rng),   # popular -> like(jack,bob)
        (1, 2): or_factor(rng),   # lonely  -> like(jack,jill)  [shared]
        (2, 4): or_factor(rng),   # like(jack,jill) -> date(jack,jill)
        (3, 5): or_factor(rng),   # like(jack,bob)  -> date(jack,bob)
        (4, 1): rng.uniform(0.1, 1.0, (2, 2)),  # date(jack,jill) -> lonely(jack) [loop]
    }
    return FactorGraph(
        n_vars=6,
        edges=[(0, 2), (0, 3), (1, 2), (2, 4), (3, 5), (4, 1)],
        factors=factors,
    )

def run(n_trials: int = 100):
    console.print("[bold cyan]QBBN Chain Experiment[/bold cyan]")
    console.print("Two grounded rules sharing an entity. Six variables, one loop.\n")

    results = []
    for seed in range(n_trials):
        g = qbbn_chain_graph(seed=seed)
        exact = g.exact_marginals()
        bp_beliefs, n_iters, converged = run_loopy_bp(g)
        kl = kl_divergence(exact, bp_beliefs)
        error = mae(exact, bp_beliefs)
        results.append((converged, n_iters, kl, error))

    n_converged = sum(r[0] for r in results)
    avg_iters = np.mean([r[1] for r in results if r[0]])
    avg_kl = np.mean([r[2] for r in results if r[0]])
    avg_mae = np.mean([r[3] for r in results if r[0]])

    table = Table(title="QBBN Chain Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Trials", str(n_trials))
    table.add_row("Converged", f"{n_converged}/{n_trials}")
    table.add_row("Avg iters (converged)", f"{avg_iters:.1f}")
    table.add_row("Avg KL divergence", f"{avg_kl:.6f}")
    table.add_row("Avg MAE", f"{avg_mae:.6f}")
    console.print(table)