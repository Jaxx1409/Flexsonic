import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Path to your log file
file_path = "data.txt"

# Regex to capture sensor values from each log line
pattern = re.compile(r"Thumb: (\d+) \| Index: (\d+) \| Middle: (\d+) \| Ring: (\d+) \| Pinky: (\d+)")

# Lists for values
thumb, index, middle, ring, pinky = [], [], [], [], []

with open(file_path, "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            t, i, m, r, p = map(int, match.groups())
            thumb.append(t)
            index.append(i)
            middle.append(m)
            ring.append(r)
            pinky.append(p)

# Put into DataFrame
df = pd.DataFrame({
    "Thumb": thumb,
    "Index": index,
    "Middle": middle,
    "Ring": ring,
    "Pinky": pinky
})

print("Data sample:\n", df.head())

# --- KMeans Clustering ---
k = 3  # number of clusters (adjust as you like)
kmeans = KMeans(n_clusters=k, random_state=42)
df["cluster"] = kmeans.fit_predict(df[["Thumb", "Index", "Middle", "Ring", "Pinky"]])

# --- Plot results (using 2 features just for visualization) ---
plt.figure(figsize=(8,6))

# Example: plot Index vs Middle, color by cluster
plt.scatter(df["Index"], df["Middle"], c=df["cluster"], cmap="viridis", s=50)

# Mark cluster centers (in Index vs Middle space)
centers = kmeans.cluster_centers_
plt.scatter(centers[:,1], centers[:,2], c="red", marker="X", s=200, label="Centroids")

plt.xlabel("Index Flex Value")
plt.ylabel("Middle Flex Value")
plt.title("K-Means Clustering on Flex Data")
plt.legend()
plt.show()
