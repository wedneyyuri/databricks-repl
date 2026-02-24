# Iris Classification — End-to-End ML Pipeline

## Prompt

> Train a RandomForest classifier on the Iris dataset. Load it into a Spark DataFrame, split into train/test, train the model, evaluate accuracy, and persist the model and metadata to a Volume.

## What Happened

Claude used the `databricks-repl` skill to execute a complete end-to-end ML pipeline in 5 steps:

1. **Load data** (7.4s) — Load sklearn's Iris dataset, convert to Spark DataFrame, print schema and statistics
2. **Preprocess** (1.0s) — Perform 70/30 train/test split, extract feature columns for scikit-learn
3. **Train** (3.3s) — Train RandomForestClassifier with 100 estimators, display feature importances
4. **Evaluate** (0.9s) — Calculate test accuracy: 88.9%
5. **Persist** (2.9s) — Save trained model (joblib) and metadata (JSON) to a Databricks Volume

The pipeline demonstrates key ML workflow steps: data loading, preprocessing, training, evaluation, and model persistence, all orchestrated through the Databricks REPL.

**Total Pipeline Time:** ~15.5 seconds

## Generated Files

All files in this directory were **automatically generated** by the `databricks-repl` skill — they are not hand-written:

- `session.json` — Session manifest with all 5 steps
- `repl_outputs/001_load_data.cmd.py` through `005_persist_model.cmd.py` — The executed code
- Corresponding `.stdout` and `.stderr` files for each step
