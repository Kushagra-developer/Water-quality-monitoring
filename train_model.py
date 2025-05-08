import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Sample water data
data = pd.DataFrame({
    'ph': [7.2, 6.8, 8.1, 7.4, 5.6, 8.5, 6.5],
    'tds': [300, 280, 220, 330, 400, 150, 500],
    'turbidity': [1.2, 1.0, 0.9, 1.5, 2.0, 0.5, 2.5],
    'temperature': [27, 26, 28, 25, 30, 24, 32],
    'label': ['Good', 'Good', 'Excellent', 'Poor', 'Hazardous', 'Excellent', 'Hazardous']
})
# Train the model
X = data[['ph', 'tds', 'turbidity', 'temperature']]
y = data['label']
model = RandomForestClassifier()
model.fit(X, y)
# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)
# Save the model
joblib.dump(model, 'model/water_quality_model.pkl')
print("✅ Model trained and saved at 'model/water_quality_model.pkl'!")
