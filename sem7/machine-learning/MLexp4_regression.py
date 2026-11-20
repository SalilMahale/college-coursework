import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ---------- 1. Load the dataset ----------
df = pd.read_csv("Housing.csv")
print("Dataset shape:", df.shape)
print(df.head())

# ---------- 2. Encode categorical (yes/no) columns ----------
binary_cols = ['mainroad', 'guestroom', 'basement',
               'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_cols:
    df[col] = df[col].map({'yes': 1, 'no': 0})

# furnishingstatus has 3 categories -> map to ordered numbers
df['furnishingstatus'] = df['furnishingstatus'].map(
    {'unfurnished': 0, 'semi-furnished': 1, 'furnished': 2})

# ---------- 3. Split features (X) and target (y) ----------
X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# max_depth=4 -> keeps the tree readable and avoids overfitting
reg_tree = DecisionTreeRegressor(criterion='squared_error',
                                 max_depth=5, random_state=42)
reg_tree.fit(X_train, y_train)

# ---------- 5. Evaluate on the test set ----------
y_pred = reg_tree.predict(X_test)
print("\n--- Regression Tree Performance ---")
print("R2 Score :", round(r2_score(y_test, y_pred), 4))
print("MAE      :", round(mean_absolute_error(y_test, y_pred), 2))
print("RMSE     :", round(mean_squared_error(y_test, y_pred) ** 0.5, 2))

# ---------- 6. Visualise the tree ----------
plt.figure(figsize=(26, 12))
plot_tree(reg_tree, feature_names=X.columns, filled=True,
          rounded=True, fontsize=8)
plt.title("CART Regression Tree - House Price Prediction (max_depth=5)")
plt.savefig("cart_regression_tree.png", dpi=150, bbox_inches='tight')
plt.show()

# ---------- 7. Feature importance ----------
importance = pd.Series(reg_tree.feature_importances_,
                       index=X.columns).sort_values(ascending=False)
print("\n--- Feature Importances ---")
print(importance)

# ---------- 8. Predict price of a NEW house ----------
new_house = pd.DataFrame([{
    'area': 6000, 'bedrooms': 3, 'bathrooms': 2, 'stories': 2,
    'mainroad': 1, 'guestroom': 0, 'basement': 1,
    'hotwaterheating': 0, 'airconditioning': 1, 'parking': 2,
    'prefarea': 1, 'furnishingstatus': 2
}])
predicted_price = reg_tree.predict(new_house)[0]
print("\nPredicted price of the new house: Rs.", round(predicted_price, 2))