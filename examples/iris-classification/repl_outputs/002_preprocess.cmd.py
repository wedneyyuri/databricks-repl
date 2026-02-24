from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

pdf_all = df.toPandas()
feature_cols = [c for c in pdf_all.columns if c not in ("label", "species")]

X = pdf_all[feature_cols].values
y = pdf_all["label"].values
label_names = dict(enumerate(load_iris().target_names))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
print(f"Train size: {len(X_train)}")
print(f"Test size:  {len(X_test)}")
print(f"Features:   {feature_cols}")
print(f"Classes:    {list(label_names.values())}")