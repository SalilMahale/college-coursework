"""
Experiment 6 - Support Vector Machine (SVM)
Dataset: diabetes_clean_10000.csv (BRFSS 2021 Health Indicators, balanced 5000/5000)
Target : Diabetes_binary (0 = No Diabetes, 1 = Diabetes)
Author : Salil Mahale | BE CMPN B | Roll No. 53
"""

import time
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, ConfusionMatrixDisplay, classification_report, RocCurveDisplay
)

# ---------------------------------------------------------------------------
# STEP 1: Load dataset and separate features / target
# ---------------------------------------------------------------------------
DATA_PATH = "diabetes_clean_10000.csv"   # <-- change only if you move the file

df = pd.read_csv(DATA_PATH)
print("Dataset Shape:", df.shape)
print("\nFirst 5 Records:")
print(df.head())

print("\nClass Distribution:")
print(df["Diabetes_binary"].value_counts())

X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"].astype(int)

print("\nTotal Records:", len(X))
print("Total Features:", X.shape[1])

# ---------------------------------------------------------------------------
# STEP 2: Build SVM pipelines (StandardScaler + SVC) for three kernels
# ---------------------------------------------------------------------------
kernels = {
    "Linear": SVC(kernel="linear", C=1.0, random_state=42, cache_size=1000),
    "Polynomial": SVC(kernel="poly", degree=3, C=1.0, gamma="scale",
                       random_state=42, cache_size=1000),
    "RBF": SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42, cache_size=1000),
}

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

scoring = {
    "accuracy": "accuracy",
    "roc_auc": "roc_auc",
    "f1": "f1",
    "precision": "precision",
    "recall": "recall",
}

# ---------------------------------------------------------------------------
# STEP 3: 10-fold stratified cross-validation for each kernel
# ---------------------------------------------------------------------------
cv_summary = []
oof_store = {}   # store out-of-fold predictions/scores per kernel for later plots

for name, estimator in kernels.items():
    print("\n" + "=" * 70)
    print(f"10-FOLD STRATIFIED CROSS VALIDATION - {name} KERNEL")
    print("=" * 70)

    pipe = Pipeline([("scaler", StandardScaler()), ("classifier", estimator)])

    t0 = time.time()
    cv_results = cross_validate(pipe, X, y, cv=cv, scoring=scoring, n_jobs=-1)
    elapsed = time.time() - t0

    row = {
        "Model": f"SVM ({name})",
        "AUC": cv_results["test_roc_auc"].mean(),
        "Accuracy": cv_results["test_accuracy"].mean(),
        "F1": cv_results["test_f1"].mean(),
        "Precision": cv_results["test_precision"].mean(),
        "Recall": cv_results["test_recall"].mean(),
        "Time(s)": round(elapsed, 1),
    }
    cv_summary.append(row)
    print(pd.DataFrame([row]).round(4).to_string(index=False))

    # Out-of-fold predictions (only needed in detail for the RBF kernel report,
    # but computed for all three so you can compare confusion matrices too)
    y_pred = cross_val_predict(pipe, X, y, cv=cv, method="predict", n_jobs=-1)
    y_score = cross_val_predict(pipe, X, y, cv=cv, method="decision_function", n_jobs=-1)
    oof_store[name] = (y_pred, y_score)

cv_summary_df = pd.DataFrame(cv_summary)
print("\n" + "=" * 70)
print("KERNEL COMPARISON SUMMARY (mean over 10 folds)")
print("=" * 70)
print(cv_summary_df.round(4).to_string(index=False))

# ---------------------------------------------------------------------------
# STEP 4: Detailed out-of-fold evaluation for the BEST kernel (by accuracy)
# ---------------------------------------------------------------------------
best_row = cv_summary_df.loc[cv_summary_df["Accuracy"].idxmax()]
best_name = best_row["Model"].replace("SVM (", "").replace(")", "")
y_pred, y_score = oof_store[best_name]

print("\n" + "=" * 70)
print(f"SUPPORT VECTOR MACHINE - {best_name} KERNEL (BEST MODEL)")
print("10-FOLD OUT-OF-FOLD RESULTS")
print("=" * 70)

svm_accuracy = accuracy_score(y, y_pred)
svm_precision = precision_score(y, y_pred, zero_division=0)
svm_recall = recall_score(y, y_pred, zero_division=0)
svm_f1 = f1_score(y, y_pred, zero_division=0)
svm_auc = roc_auc_score(y, y_score)

print("\nAccuracy :", round(svm_accuracy, 4))
print("Precision:", round(svm_precision, 4))
print("Recall   :", round(svm_recall, 4))
print("F1 Score :", round(svm_f1, 4))
print("AUC      :", round(svm_auc, 4))

print("\nClassification Report:")
print(classification_report(y, y_pred, target_names=["No Diabetes", "Diabetes"], zero_division=0))

svm_cm = confusion_matrix(y, y_pred)
print("Confusion Matrix:")
print(svm_cm)
print("Total Confusion Matrix Records:", svm_cm.sum())

# ---------------------------------------------------------------------------
# STEP 5: Plots
# ---------------------------------------------------------------------------
# 5a. Confusion matrix
ConfusionMatrixDisplay.from_predictions(
    y, y_pred,
    display_labels=["No Diabetes", "Diabetes"],
    values_format="d",
    cmap="Greys",
)
plt.title(f"Confusion Matrix - SVM ({best_name} Kernel)")
plt.tight_layout()
plt.savefig("confusion_matrix_svm.png", dpi=150)
plt.show()

# 5b. ROC curve for the best kernel
RocCurveDisplay.from_predictions(y, y_score, name=f"SVM ({best_name})")
plt.plot([0, 1], [0, 1], "k--", label="Chance")
plt.title(f"ROC Curve - SVM ({best_name} Kernel)")
plt.legend()
plt.tight_layout()
plt.savefig("roc_curve_svm.png", dpi=150)
plt.show()

# 5c. Kernel comparison bar chart
cv_summary_df.set_index("Model")[["Accuracy", "F1", "Precision", "Recall"]].plot(
    kind="bar", figsize=(10, 6)
)
plt.title("SVM Performance Comparison Across Kernels")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.legend()
plt.tight_layout()
plt.savefig("kernel_comparison_svm.png", dpi=150)
plt.show()

# ---------------------------------------------------------------------------
# STEP 6: Final result
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("FINAL RESULT")
print("=" * 70)
print("\nBest Kernel Based on Cross-Validation Accuracy:", best_name)
print("Accuracy:", round(best_row["Accuracy"], 4))
print("Accuracy (%):", round(best_row["Accuracy"] * 100, 2), "%")
