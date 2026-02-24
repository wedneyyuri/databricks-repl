import joblib
import os
import json

workspace_dir = "/Volumes/catalog/schema/vol/iris-classification"
os.makedirs(workspace_dir, exist_ok=True)

model_path = os.path.join(workspace_dir, "model.pkl")
meta_path = os.path.join(workspace_dir, "meta.json")

if os.path.exists(model_path):
    print(f"Model already exists at {model_path}, skipping save.")
    model = joblib.load(model_path)
else:
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

meta = {
    "feature_cols": feature_cols,
    "label_names": {str(k): str(v) for k, v in label_names.items()},
    "train_size": len(X_train),
    "test_size": len(X_test),
    "test_accuracy": float(test_acc),
}
with open(meta_path, "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved to {meta_path}")
print(json.dumps(meta, indent=2))