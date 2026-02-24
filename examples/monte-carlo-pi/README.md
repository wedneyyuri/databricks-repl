# Monte Carlo Pi — Distributed Spark Estimation

## Prompt

> Estimate Pi using a Monte Carlo simulation with PySpark. Start with 100 million samples, then scale to 1 billion and 10 billion to show how accuracy improves with more samples.

## What Happened

Claude used the `databricks-repl` skill to run 3 progressively larger simulations demonstrating how increased sample size improves the accuracy of the Pi estimation:

| Step | Samples | Time | Pi Estimate | Error |
|------|---------|------|-------------|-------|
| 1 | 100M | 10.7s | ~3.14159 | ~0.00001 |
| 2 | 1B | 10.3s | ~3.14159 | ~0.000003 |
| 3 | 10B | 79.8s | ~3.14159 | ~0.0000005 |

Each step uses `spark.range()` to generate random (x, y) coordinates, counts points inside the unit circle (where x² + y² ≤ 1), and computes `4 × (inside / total)` to estimate Pi.

The distributed nature of Spark allows the 1 billion sample calculation to complete in roughly the same time as 100 million samples, demonstrating horizontal scalability.

## Generated Files

All files in this directory were **automatically generated** by the `databricks-repl` skill — they are not hand-written:

- `session.json` — Session manifest with step metadata
- `repl_outputs/001_monte_carlo.cmd.py` — 100M samples
- `repl_outputs/002_monte_carlo_1b.cmd.py` — 1B samples
- `repl_outputs/003_monte_carlo_10b.cmd.py` — 10B samples
- Corresponding `.stdout` and `.stderr` files for each step
