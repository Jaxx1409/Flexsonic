# preprocess_train_kmeans.py
# Usage: python preprocess_train_kmeans.py data_processed/gesture_parsed.csv

import argparse, os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import joblib

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--k", type=int, default=3, help="Number of clusters (gestures)")
args = parser.parse_args()

df = pd.read_csv(args.infile)

# Ensure expected columns exist
flex_cols = ["Thumb","Index","Middle","Ring","Pinky"]
for c in flex_cols:
    if c not in df.columns:
        df[c] = 0

# Drop rows where all flex values are zero (likely noise)
df = df[df[flex_cols].sum(axis=1) > 0].reset_index(drop=True)
print("Rows after cleaning:", len(df))

# Features (you can add gyro cols later)
X = df[flex_cols].astype(float).values

# Scale: KMeans uses distances, so scaling makes features comparable.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# KMeans
k = args.k
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X_scaled)
labels = kmeans.labels_

df["cluster"] = labels

# Save model + scaler
os.makedirs("../models", exist_ok=True)
joblib.dump(kmeans, "../models/kmeans.pkl")
joblib.dump(scaler, "../models/scaler.pkl")
print("Saved kmeans and scaler to ../models/")

# Save labelled CSV
out_csv = os.path.join("data processed","data_with_clusters.csv")
df.to_csv(out_csv, index=False)
print("Saved labelled data to:", out_csv)

# Visualize using PCA -> 2D
pca = PCA(n_components=2)
reduced = pca.fit_transform(X_scaled)

# Project cluster centers into PCA space for plotting
centers_pca = pca.transform(kmeans.cluster_centers_)

plt.figure(figsize=(8,6))
scatter = plt.scatter(reduced[:,0], reduced[:,1], c=labels, cmap="tab10", s=30)
plt.scatter(centers_pca[:,0], centers_pca[:,1], c="black", marker="X", s=150, label="centroids")
plt.title(f"KMeans (k={k}) on flex data (PCA projection)")
plt.xlabel("PC1"); plt.ylabel("PC2")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("ml","kmeans_clusters.png"), dpi=150)
print("Saved PCA cluster plot to ml/kmeans_clusters.png")
plt.show()
