import pandas as pd

# Load clustered data
df = pd.read_csv("data processed/data_with_clusters.csv")

# Map cluster IDs to gesture labels
label_map = {
    2: "middle_bent",
    1: "index_bent",
    0: "null"
    # add more if needed
}
df["gesture"] = df["cluster"].map(label_map)

# Save labeled dataset
df.to_csv("data processed/gesture_labeled.csv", index=False)

print("✅ gesture_labeled.csv regenerated with labels")
