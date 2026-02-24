# Eviction & Replay

## Table of Contents

- [What Is Eviction](#what-is-eviction)
- [Detection](#detection)
- [Eviction Response Format](#eviction-response-format)
- [Replay Strategies](#replay-strategies)
- [Idempotent Replay Examples](#idempotent-replay-examples)

---

## What Is Eviction

Databricks automatically garbage-collects idle execution contexts. When this happens:

- All in-memory Python state is gone (variables, loaded data, trained models)
- The cluster itself is still running
- `.cmd.py` files and `session.json` on disk are unaffected
- Files previously written to Volumes are unaffected

Eviction is permanent for that context. Recovery requires creating a fresh context and replaying commands.

---

## Detection

The wrapper detects eviction lazily — when a submit fails because the context no longer exists. It does not proactively ping the context before each command.

When eviction is detected, the wrapper automatically:
1. Creates a new execution context on the same cluster
2. Re-injects the bootstrap helpers
3. Returns a structured eviction response (instead of the normal exec response)

---

## Eviction Response Format

When an `exec` call triggers eviction detection, the response looks like:

```json
{
  "status": "ContextEvicted",
  "message": "Execution context was evicted. Fresh context created. Replay needed.",
  "new_context_id": "xyz789...",
  "project_dir": ".",
  "previous_steps": [
    {
      "step": 1,
      "tag": "install_deps",
      "command_file": "./repl_outputs/001_install_deps.cmd.py"
    },
    {
      "step": 2,
      "tag": "load_data",
      "command_file": "./repl_outputs/002_load_data.cmd.py"
    },
    {
      "step": 3,
      "tag": "train",
      "command_file": "./repl_outputs/003_train.cmd.py"
    },
    {
      "step": 4,
      "tag": "evaluate",
      "command_file": "./repl_outputs/004_evaluate.cmd.py"
    }
  ]
}
```

Key fields:
- `previous_steps` — ordered list of all steps from the evicted session
- `command_file` — path to the original `.cmd.py` source for each step

---

## Replay Strategies

You (the root LM) decide how to replay. The wrapper does not classify, prioritize, or generate restore scripts. Use these strategies based on each step's characteristics:

### Strategy 1: Replay As-Is

For steps that are naturally idempotent — data loading, evaluation, exploratory queries.

```bash
# Read the original command and re-execute it unchanged
python .claude/skills/databricks-repl/dbx_repl.py exec \
  --command @./repl_outputs/002_load_data.cmd.py \
  --tag "load_data"
```

### Strategy 2: Conditional Load from Volume

For steps that previously wrote expensive results to a Volume. Load from Volume if the file exists; otherwise recompute.

Read the original `.cmd.py`, then wrap the expensive computation in a conditional check. See [examples below](#idempotent-replay-examples).

### Strategy 3: Install Steps (Always Replay)

`%pip install` is naturally idempotent. Always replay install steps as-is.

```bash
python .claude/skills/databricks-repl/dbx_repl.py exec \
  --command @./repl_outputs/001_install_deps.cmd.py \
  --tag "install_deps"
```

### Replay Order

Replay steps in their original order. Dependencies between steps (e.g., step 3 uses a DataFrame loaded in step 2) require sequential replay.

Typical replay sequence:
1. Install steps first (idempotent)
2. Data loading steps (replay as-is)
3. Expensive compute steps (conditional load from Volume)
4. The command that was interrupted by eviction (re-execute)

---

## Idempotent Replay Examples

### Training step with saved model

**Original command (from `.cmd.py`):**

```python
from sklearn.ensemble import RandomForestClassifier
import joblib

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
joblib.dump(model, "/Volumes/catalog/schema/vol/model.pkl")
```

**Idempotent replay version:**

```python
import os
import joblib

volume_path = "/Volumes/catalog/schema/vol/model.pkl"
if os.path.exists(volume_path):
    model = joblib.load(volume_path)
    print(f"Loaded model from {volume_path}")
else:
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, volume_path)
```

### DataFrame processing with saved output

**Original command:**

```python
predictions_df = model.transform(test_df)
predictions_pdf = predictions_df.toPandas()
predictions_pdf.to_parquet("/Volumes/catalog/schema/vol/predictions.parquet", index=False)
```

**Idempotent replay version:**

```python
import os
import pandas as pd

volume_path = "/Volumes/catalog/schema/vol/predictions.parquet"
if os.path.exists(volume_path):
    predictions_pdf = pd.read_parquet(volume_path)
    print(f"Loaded predictions from {volume_path}")
else:
    predictions_df = model.transform(test_df)
    predictions_pdf = predictions_df.toPandas()
    predictions_pdf.to_parquet(volume_path, index=False)
```

### Multiple outputs in one step

When a step saves multiple files, check all of them:

```python
import os
import joblib, json

model_path = "/Volumes/catalog/schema/vol/model.pkl"
metrics_path = "/Volumes/catalog/schema/vol/metrics.json"

if os.path.exists(model_path) and os.path.exists(metrics_path):
    model = joblib.load(model_path)
    with open(metrics_path) as f:
        metrics = json.load(f)
    print("Loaded model and metrics from Volumes")
else:
    # Full training + evaluation pipeline
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    joblib.dump(model, model_path)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
```
