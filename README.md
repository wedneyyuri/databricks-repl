# databricks-repl

Genie gives you AI inside Databricks. This gives you Databricks inside AI.

Run code on Databricks clusters while your agent orchestrates everything else — other skills, subagents, MCPs, local files, and parallel hypothesis validation. One session, no boundaries.

Works with Claude Code, Cursor, GitHub Copilot, and [35+ other agents](https://agentskills.io).

## Add Databricks to Your Agent

```bash
claude plugin add wedneyyuri/databricks-repl
```

## Genie vs. Full Orchestration

Genie works inside one notebook, one workspace. When the real work crosses boundaries, it stops. Your AI agent doesn't.

| What you need | Genie | Your agent + this skill |
|---------------|-------|------------------------|
| Analyze a repo and cross-reference with Databricks logs | Workspace only | Reads repo + queries cluster in one session |
| Validate 3 hypotheses in parallel on different datasets | One notebook at a time | Spawns subagents, each running its own cluster query |
| Train on cluster, compare with local baselines, commit results | Can't access local files or git | Cluster compute + local files + git — same session |
| Use an MCP to enrich data before running Spark | No MCP support | Calls MCPs, APIs, other skills, then sends to cluster |
| Explore Python + Scala + SQL across multiple repos | Single-language notebooks | Subagents explore each language, agent synthesizes |
| Resume after cluster eviction | Start over | Append-only session log with replay |

The difference isn't features. It's architecture. Genie is an assistant scoped to Databricks. This makes Databricks one resource inside an orchestrator that can do **anything** — use [GSD](https://github.com/coreyhaines31/get-shit-done), [superpowers](https://github.com/coreyhaines31/superpowers), compose skills, spawn subagents, interact with MCPs, and parallelize work across tools.

## What It Looks Like

```
You: "Load the customers table, train a classifier,
      compare with last quarter's local baseline,
      and open a PR with the results"

Claude:
→ creates a REPL session on your Databricks cluster
→ runs the training code, captures outputs as files
→ reads your local baseline for comparison
→ consolidates everything into a clean .py file
→ commits and opens the PR
```

Five tools, one session. No switching between terminal, notebooks, and browser.

## How It Works

1. **You describe the task** — your agent decides what to run
2. **Scripts handle the plumbing** — auth, sessions, polling, output capture
3. **Agent sees only metadata** — file paths and status, never raw output

Context stays clean. Sessions stay productive for 50+ interactions.

## Examples

| Example | What It Shows |
|---------|---------------|
| [primes](examples/primes/) | Basic Python execution on a Databricks cluster |
| [monte-carlo-pi](examples/monte-carlo-pi/) | Distributed Spark — estimate π scaling from 100M to 10B samples |
| [iris-classification](examples/iris-classification/) | Full ML pipeline — load, train, evaluate, persist model to Volumes |

## Skills

| Skill | What It Does |
|-------|--------------|
| [databricks-repl](skills/databricks-repl/) | Execute Python on Databricks via a stateful REPL session |
| [databricks-repl-consolidate](skills/databricks-repl-consolidate/) | Turn a REPL session into a single committable .py file |

## Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/install.html) with a profile in `~/.databrickscfg`
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html) (`pip install databricks-sdk`)
- A running classic all-purpose cluster

## Using with Other Agents

These skills follow the [Agent Skills Specification](https://agentskills.io/specification). Copy `skills/` to wherever your agent reads SKILL.md files.

### Cursor

```bash
cp -r skills/databricks-repl .cursor/skills/
cp -r skills/databricks-repl-consolidate .cursor/skills/
```

### GitHub Copilot

```bash
mkdir -p .github/skills
cp -r skills/databricks-repl .github/skills/
cp -r skills/databricks-repl-consolidate .github/skills/
```

## Start Orchestrating

Databricks is powerful. But Databricks inside an AI agent that can parallelize work, compose tools, and cross every boundary? That's something else.

```bash
claude plugin add wedneyyuri/databricks-repl
```

## License

[MIT](LICENSE)
