import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, ConfusionMatrixDisplay)

# ---------- 1. Load the dataset ----------
df = pd.read_csv("diabetes_binary_5050split_health_indicators_BRFSS2021.csv")
print("Dataset shape:", df.shape)
print(df['Diabetes_binary'].value_counts())   # balanced 50-50 split

# ---------- 2. Split features (X) and target (y) ----------
X = df.drop('Diabetes_binary', axis=1)
y = df['Diabetes_binary']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# max_depth=4 -> keeps the tree readable and prevents overfitting
clf_tree = DecisionTreeClassifier(criterion='gini',
                                  max_depth=4, random_state=42)
clf_tree.fit(X_train, y_train)

# ---------- 4. Evaluate on the test set ----------
y_pred = clf_tree.predict(X_test)
print("\n--- Classification Tree Performance ---")
print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n",
      classification_report(y_test, y_pred,
                            target_names=['No Diabetes', 'Diabetes']))

# ---------- 5. Visualise the confusion matrix ----------
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, display_labels=['No Diabetes', 'Diabetes'], cmap='Blues')
plt.title("Confusion Matrix - CART Classifier")
plt.savefig("cart_confusion_matrix.png", dpi=150, bbox_inches='tight')
plt.show()

# ---------- 6. Visualise the tree ----------
plt.figure(figsize=(26, 12))
plot_tree(clf_tree, feature_names=X.columns,
          class_names=['No Diabetes', 'Diabetes'],
          filled=True, rounded=True, fontsize=8)
plt.title("CART Classification Tree - Diabetes Prediction (max_depth=4)")
plt.savefig("cart_classification_tree.png", dpi=150, bbox_inches='tight')
plt.show()

# ---------- 7. Feature importance ----------
importance = pd.Series(clf_tree.feature_importances_,
                       index=X.columns).sort_values(ascending=False)
print("\n--- Top 10 Feature Importances ---")
print(importance.head(10))

# ---------- 8. Predict for a NEW patient ----------
new_patient = pd.DataFrame([{
    'HighBP': 1, 'HighChol': 1, 'CholCheck': 1, 'BMI': 32.0,
    'Smoker': 1, 'Stroke': 0, 'HeartDiseaseorAttack': 0,
    'PhysActivity': 0, 'Fruits': 0, 'Veggies': 1,
    'HvyAlcoholConsump': 0, 'AnyHealthcare': 1, 'NoDocbcCost': 0,
    'GenHlth': 4, 'MentHlth': 5, 'PhysHlth': 10, 'DiffWalk': 1,
    'Sex': 1, 'Age': 9, 'Education': 5, 'Income': 6
}])
prediction = clf_tree.predict(new_patient)[0]
probability = clf_tree.predict_proba(new_patient)[0]
print("\nNew patient prediction:",
      "Diabetes" if prediction == 1 else "No Diabetes")
print("Probability [No Diabetes, Diabetes]:", probability.round(3))