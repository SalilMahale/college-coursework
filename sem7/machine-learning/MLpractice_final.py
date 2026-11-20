import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, root_mean_squared_error, r2_score

df = pd.read_csv('house_price_regression_dataset.csv')

corr = df.corr(method='pearson')
print(corr)

df_X = df[['Square_Footage', 'Num_Bedrooms', 'Num_Bathrooms', 'Year_Built',
           'Lot_Size', 'Garage_Size', 'Neighborhood_Quality']]
df_Y = df['House_Price']

df_X_train, df_X_test, df_Y_train, df_Y_test = train_test_split(
    df_X, df_Y, train_size=0.8, random_state=42)

regmodel = LinearRegression()
regmodel.fit(df_X_train, df_Y_train)

y_pred = regmodel.predict(df_X_test)

result = pd.DataFrame({
    'Actual': df_Y_test.values,
    'Predicted': np.round(y_pred, 2)
})
print("\nActual vs Predicted (first 10 rows)")
print("------------------------------------")
print(result.head(10))

mse = mean_squared_error(df_Y_test, y_pred)
rmse = root_mean_squared_error(df_Y_test, y_pred)
r2 = r2_score(df_Y_test, y_pred)

print("\nPerformance Metrics")
print("-------------------")
print("MSE :", mse)
print("RMSE:", rmse)
print("R2  :", r2)

print("\nModel Coefficients")
print("-------------------")
for feature, coef in zip(df_X.columns, regmodel.coef_):
    print(f"  {feature}: {coef:.4f}")
print(f"Intercept: {regmodel.intercept_:.4f}")

plt.figure(figsize=(7, 6))
plt.imshow(corr, cmap='coolwarm')
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Matrix - House Price Dataset")
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150)
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(df_Y_test, y_pred, alpha=0.6, edgecolor='k')
plt.xlabel("Actual House Price")
plt.ylabel("Predicted House Price")
plt.title("Actual vs Predicted House Price")
plt.plot([df_Y.min(), df_Y.max()],
         [df_Y.min(), df_Y.max()],
         color='red', linewidth=2, label='Ideal fit (y = x)')
plt.legend()
plt.tight_layout()
plt.savefig('actual_vs_predicted.png', dpi=150)
plt.show()
