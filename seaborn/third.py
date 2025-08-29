# Step 1: Libraries import karo
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Step 2: Sample dataset create karo
data = {
    'Size': [500, 700, 900, 1000, 1200, 1500, 1800],
    'Price': [150000, 200000, 250000, 275000, 325000, 400000, 450000]
}

df = pd.DataFrame(data)

# Step 3: Features and target define karo
X = df[['Size']]    # Feature (independent variable)
y = df['Price']     # Target (dependent variable)

# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Model create karo
model = LinearRegression()

# Step 6: Train the model
model.fit(X_train, y_train)

# Step 7: Prediction karo (test data pe)
y_pred = model.predict(X_test)

# Step 8: Result dekho (float me convert karke)
print("Actual Prices:", list(y_test))
print("Predicted Prices:", [float(p) for p in y_pred])

# Step 9: Model performance
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Step 10: New prediction (warning fix ke saath)
new_house_size = pd.DataFrame({'Size':[1300]})
predicted_price = model.predict(new_house_size)
print(f"Predicted price for house of 1300 sq ft: ${float(predicted_price[0]):.2f}")
