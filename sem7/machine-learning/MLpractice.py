import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,root_mean_squared_error,r2_score

df = pd.read_csv('house_price_regression_dataset.csv')

# print(df.corr(method='pearson'))

df_X = df[['Square_Footage','Num_Bedrooms','Num_Bathrooms','Year_Built','Lot_Size','Garage_Size','Neighborhood_Quality']]
df_Y = df['House_Price']

df_X_train, df_X_test, df_Y_train, df_Y_test = train_test_split(df_X, df_Y, train_size=0.8, random_state=42)

regmodel = LinearRegression()
regmodel.fit(df_X_train,df_Y_train)

print(mean_squared_error(regmodel.predict(df_X_test), df_Y_test))
print(root_mean_squared_error(regmodel.predict(df_X_test), df_Y_test))
print(r2_score(regmodel.predict(df_X_test), df_Y_test))

