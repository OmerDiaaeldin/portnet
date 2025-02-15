import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from lightgbm import LGBMClassifier

# Suppress warnings
warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv("/content/enhanced_predictive_maintenance_cranes.csv")

# Drop timestamp column (not needed for ML models)
df.drop(columns=["Timestamp"], inplace=True)

# Define features (X) and target variable (y)
X = df.drop(columns=["Maintenance_Needed"])  # All sensor readings
y = df["Maintenance_Needed"]  # Target variable

# Split data into training (80%) and test (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features for better model performance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train an LGBM model
model = LGBMClassifier(n_estimators=200, learning_rate=0.05, max_depth=10, random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Model Training Completed!")
print(f"Model Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Generate confusion matrix and heatmap
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['No Maintenance', 'Maintenance'], yticklabels=['No Maintenance', 'Maintenance'])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Print classification report
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Function to predict maintenance need on new data
def predict_maintenance(new_data):
    new_data = np.array(new_data).reshape(1, -1)  # Ensure correct shape
    new_data_scaled = scaler.transform(new_data)
    prediction = model.predict(new_data_scaled)[0]
    return "Maintenance Required" if prediction == 1 else "No Maintenance Needed"

# Example usage (replace with real sensor readings)
example_input = X.iloc[0].values  # Taking the first row as a sample
print("Prediction for sample data:", predict_maintenance(example_input))