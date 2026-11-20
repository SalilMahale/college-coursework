"""
Experiment 7 - Multiclass Classification using SVM (Python cross-check of Weka)
Strategies compared : One-vs-One (OvO) and One-vs-Rest (OvR)
"""

import pandas as pd, time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report)

df = pd.read_csv("diabetes_multiclass_exp7.csv")
X = df.drop(columns=["HealthTier"])
y = df["HealthTier"]

# Stratified 70/30 split -> same protocol as Weka's percentage split
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.30, random_state=1, stratify=y)

base = SVC(kernel="linear", C=1.0)          # same idea as Weka SMO + PolyKernel E=1

for name, model in [("One-vs-One (OvO)", OneVsOneClassifier(base)),
                    ("One-vs-Rest (OvR)", OneVsRestClassifier(base))]:
    clf = make_pipeline(StandardScaler(), model)   # SVMs need scaled inputs
    t0 = time.time()
    clf.fit(X_tr, y_tr)
    pred = clf.predict(X_te)
    n_models = len(clf[-1].estimators_)
    print("=" * 62)
    print(f"{name}  |  binary models built = {n_models}"
          f"  |  train time = {time.time()-t0:.1f}s")
    print(f"Accuracy = {accuracy_score(y_te, pred)*100:.2f}%")
    print("Confusion matrix (rows = actual, cols = predicted):")
    print(pd.DataFrame(confusion_matrix(y_te, pred),
                       index=sorted(y.unique()), columns=sorted(y.unique())))
    print(classification_report(y_te, pred, digits=3))
