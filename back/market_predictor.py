import pandas as pd
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import datetime

# Load the dataset
df = pd.read_csv("/content/import_data(2).csv")

# Ensure date column exists and convert it to datetime format if applicable
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
else:
    raise ValueError("Dataset must contain a 'date' column for accurate predictions.")

# Encode categorical features
label_encoders = {}
for col in ["goods_type", "country_of_origin"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target
features = [
    "goods_type", "country_of_origin", "import_declarations", "value_declared",
    "month", "day", "day_of_week", "exchange_rate", "shipping_cost_index", "port_congestion",
    "active_ships", "container_availability", "weather_disruption", "economic_disruption"
]
target = "import_volume"

# Check for missing values and fill if necessary
df.fillna(df.median(), inplace=True)

X = df[features]
y = df[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train LightGBM model
lgb_train = lgb.Dataset(X_train, label=y_train)
lgb_test = lgb.Dataset(X_test, label=y_test, reference=lgb_train)

params = {
    'objective': 'regression',
    'metric': 'mae',
    'boosting_type': 'gbdt',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'verbose': -1
}

# Ensure compatibility with LightGBM version

model = lgb.LGBMRegressor(n_estimators=200, learning_rate=0.05, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")
print(f"R^2 Score: {r2}")

# Feature Importance Plot
plt.figure(figsize=(10, 6))
lgb.plot_importance(model, max_num_features=10)
plt.title("Feature Importance")
plt.show()

# Predicted vs Actual Plot
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
plt.xlabel("Actual Import Volume")
plt.ylabel("Predicted Import Volume")
plt.title("Actual vs Predicted Import Volume")
plt.show()

# Residual Plot
residuals = y_test - y_pred
plt.figure(figsize=(8, 6))
sns.histplot(residuals, bins=30, kde=True)
plt.xlabel("Residuals")
plt.ylabel("Frequency")
plt.title("Residual Distribution")
plt.show()

# Function to predict import volume for a specific date
def predict_import_volume(date, goods_type, country_of_origin, import_declarations, value_declared, 
                          exchange_rate, shipping_cost_index, port_congestion, active_ships, 
                          container_availability, weather_disruption, economic_disruption):
    date = pd.to_datetime(date)
    input_data = pd.DataFrame({
        "goods_type": [label_encoders["goods_type"].transform([goods_type])[0]],
        "country_of_origin": [label_encoders["country_of_origin"].transform([country_of_origin])[0]],
        "import_declarations": [import_declarations],
        "value_declared": [value_declared],
        "month": [date.month],
        "day": [date.day],
        "day_of_week": [date.dayofweek],
        "exchange_rate": [exchange_rate],
        "shipping_cost_index": [shipping_cost_index],
        "port_congestion": [port_congestion],
        "active_ships": [active_ships],
        "container_availability": [container_availability],
        "weather_disruption": [weather_disruption],
        "economic_disruption": [economic_disruption]
    })
    return model.predict(input_data)[0]

# Example prediction
example_prediction = predict_import_volume("2025-03-01", "Electronics", "China", 500, 100000, 
                                           1.1, 120, 30, 45, 80, 5, 10)
print(f"Predicted Import Volume for 2025-03-01: {example_prediction}")