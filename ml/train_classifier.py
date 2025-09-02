// WORK IN PROGRESS


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("csv_path", help="Path to gesture_labeled.csv")
args = parser.parse_args()

# Load dataset
df = pd.read_csv(args.csv_path)

# Features and labels
X = df[["Thumb", "Index", "Middle", "Ring", "Pinky"]]
y = df["gesture"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model + scaler
os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/gesture_classifier.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("✅ Model and scaler saved in models/")

df = pd.read_csv(csv_path)


