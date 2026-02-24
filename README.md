# databricks-repl

Run Python on Databricks clusters from your AI coding agent. Just describe what you want — the skill handles auth, sessions, output capture, and eviction recovery.

Works with Claude Code, Cursor, GitHub Copilot, and [35+ other agents](https://agentskills.io).

## What It Feels Like

```
You: "Load the customers table and train a classifier"

Claude:
→ creates a REPL session on your cluster
→ executes the code, returns JSON metadata
→ reads output selectively (only what matters enters context)
→ iterates until done, then consolidates into a clean .py file
```

No auth boilerplate, no polling loops, no raw API responses in your context window.

## How It Works

1. **You describe the task** — Claude decides what code to run
2. **Scripts handle the plumbing** — `dbx_repl.py` manages auth, session creation, polling, and output capture
3. **Claude sees only metadata** — JSON status + file paths, never raw output or tokens
4. **Outputs land as files** — Claude reads selectively, keeping its context clean
5. **Sessions consolidate** — when done, the full session becomes a single committable `.py` file

## Skills

| Skill | Description |
|-------|-------------|
| [databricks-repl](skills/databricks-repl/) | Execute Python on a Databricks cluster via a stateful REPL session. Covers session lifecycle (create, exec, await, cancel, destroy), output file management, eviction recovery, and recursive LM calls via `sub_llm()`. |
| [databricks-repl-consolidate](skills/databricks-repl-consolidate/) | Consolidate a Databricks REPL session into a single, clean Python file. Transforms `.cmd.py` step files into a committable script with deduplication, import resolution, and boilerplate stripping. |

## Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/install.html) configured with a profile in `~/.databrickscfg`
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html) (`pip install databricks-sdk`)
- A **classic all-purpose cluster** in running state (the Command Execution API requires it)

## Installation

### Claude Code Plugin (Recommended)

```bash
claude plugin add wedneyyuri/databricks-repl
```

### Manual Installation

Copy the skills to your project:

```bash
# Clone the repo
git clone https://github.com/wedneyyuri/databricks-repl.git /tmp/claude-databricks

# Copy skills to your project
cp -r /tmp/claude-databricks/skills/databricks-repl .claude/skills/
cp -r /tmp/claude-databricks/skills/databricks-repl-consolidate .claude/skills/
```

## Quick Start

Once installed, invoke the skill in Claude Code:

```
> Use databricks-repl with profile "default" and cluster "my-cluster"
```

Claude will:

1. **Resolve** the cluster by name
2. **Create** a stateful REPL session with bootstrap helpers
3. **Execute** your Python code, returning JSON metadata + file paths
4. **Read output selectively** — only what's needed enters Claude's context
5. **Destroy** the session when you're done

## Examples

The [`examples/`](examples/) directory contains complete sessions you can study or replay:

| Example | Complexity | What It Shows |
|---------|-----------|---------------|
| [primes](examples/primes/) | Beginner | Basic Python execution — Sieve of Eratosthenes on a Databricks cluster |
| [monte-carlo-pi](examples/monte-carlo-pi/) | Intermediate | Distributed Spark computation — estimate π with 100M → 10B samples, showing cluster scaling |
| [iris-classification](examples/iris-classification/) | Advanced | End-to-end ML pipeline — load, preprocess, train RandomForest, evaluate, persist model to Volumes |

Each example contains a `session.json` (step manifest) and `repl_outputs/` with the `.cmd.py` source and stdout/stderr for every step.

## Why This Approach?

The primary motivation is **context management** — keeping your agent's context window clean so you can work in longer sessions without compaction.

| Approach | Context Cost | Trade-off |
|----------|-------------|-----------|
| **MCP server** | Tool schemas loaded at startup, every call returns raw API responses into context | Agent must re-learn the Databricks API patterns on every invocation, bloating the context with boilerplate |
| **Direct code generation** | Agent writes full SDK code each time — auth, polling, error handling | Tokens wasted on repetitive plumbing that never changes |
| **Skills + scripts** | Instructions loaded only when needed, scripts return JSON metadata + file paths | Agent sees only what matters — no tokens wasted on auth, polling, or raw output |

This follows the [Recursive Language Model (RLM)](https://alexzhang13.github.io/blog/2025/rlm/) pattern:

- **Root LM (Claude)** reasons about the task, decides what code to run, and reads outputs selectively
- **Scripts (`dbx_repl.py`)** handle all deterministic plumbing — auth, context creation, polling, output capture — so it never enters the agent's context
- **Sub-LMs (`sub_llm()`)** execute on-cluster LLM calls for map/reduce, classification, and summarization without consuming root context

## How Is This Different from Databricks Genie?

[Databricks Genie](https://docs.databricks.com/en/genie/) is an AI assistant embedded in the Databricks workspace. It's great for what it does, but it operates in a different scope:

| Capability | Databricks Genie / Assistant | This skill (via Claude Code, Cursor, Copilot) |
|---|---|---|
| **Execute Python/SQL** | In Databricks notebooks only | On Databricks clusters, from your local terminal |
| **Access local files** | No — workspace only | Yes — full local filesystem access |
| **Cross-project context** | No — scoped to current notebook/space | Yes — combine data from git repos, local files, APIs, other skills |
| **Extend with plugins** | Limited to MCP servers in workspace | Full ecosystem — other skills, MCP servers, IDE extensions, shell tools |
| **Session continuity** | Notebook-scoped, no lineage tracking | Append-only session log with eviction replay and consolidation |
| **LLM recursion** | No `sub_llm()` pattern | Built-in `sub_llm()` / `sub_llm_batch()` for on-cluster map/reduce |
| **Work offline on results** | No — must stay in Databricks UI | Yes — outputs are local files, work continues without cluster |

The key advantage: **your coding agent becomes the orchestrator**. It can read a CSV from your desktop, run a Spark job on Databricks, compare results with a local model, commit the output to git, and open a PR — all in one session. Genie can't cross those boundaries.

## Using with Cursor or GitHub Copilot

These skills follow the [Agent Skills Specification](https://agentskills.io/specification), which is supported by Cursor, GitHub Copilot, Windsurf, Cline, and [35+ other agents](https://agentskills.io).

### Cursor

Copy the skills to your Cursor skills directory:

```bash
cp -r skills/databricks-repl .cursor/skills/
cp -r skills/databricks-repl-consolidate .cursor/skills/
```

Cursor Agent will discover and load them when relevant. Make sure `.cursor/rules/` includes a rule to activate your Python environment if needed.

### GitHub Copilot

Copy the skills to your Copilot skills directory:

```bash
mkdir -p .github/skills
cp -r skills/databricks-repl .github/skills/
cp -r skills/databricks-repl-consolidate .github/skills/
```

Copilot's agent mode will load the SKILL.md instructions when you ask it to work with Databricks.

### Any Agent with SKILL.md Support

The skills are portable. Copy the `skills/` directory to wherever your agent reads SKILL.md files — the scripts use relative paths and `Path(__file__).parent` for self-references.

## Specification

These skills follow the [Agent Skills Specification](https://agentskills.io/specification).

## License

[MIT](LICENSE)
