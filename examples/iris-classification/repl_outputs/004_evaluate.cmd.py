from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np

y_pred = model.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)

print(f"Test accuracy: {test_acc:.4f}\n")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=list(label_names.values())))
print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
header = "          " + "  ".join(f"{label_names[i]:>10}" for i in range(len(label_names)))
print(header)
for i, row in enumerate(cm):
    print(f"{label_names[i]:>10} " + "  ".join(f"{v:>10}" for v in row))

print(f"\nSample predictions (first 10):")
for i in range(min(10, len(y_test))):
    actual = label_names[y_test[i]]
    predicted = label_names[y_pred[i]]
    match = "OK" if y_test[i] == y_pred[i] else "MISS"
    print(f"  [{match}] actual={actual}, predicted={predicted}")