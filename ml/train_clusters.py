import os
import pandas as pd
import joblib
from sklearn.cluster import KMeans

# Load dataset
data = pd.read_csv("data processed/gesture_labeled.csv")

# Keep only numeric columns
X = data.select_dtypes(include=["number"])

# Train KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X)

# Ensure 'models' folder exists
os.makedirs("models", exist_ok=True)

# Save trained model
joblib.dump(kmeans, "models/gesture_clusters.pkl")
print("✅ KMeans model saved to models/gesture_clusters.pkl")
