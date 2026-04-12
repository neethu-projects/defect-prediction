import pandas as pd
import sqlite3

print("Extracting features from raw_diffs table...")

conn = sqlite3.connect("data/defect_data.db")

# Step 1 - Load raw data from DB
all_diffs = pd.read_sql("SELECT * FROM raw_diffs", conn)
print(f"Loaded {len(all_diffs)} rows from raw_diffs")

# Step 2 - Group by filename
grouped = all_diffs.groupby("filename")

# Step 3 - Extract features
dataset = pd.DataFrame({
    "commit_count":    grouped["date"].count(),
    "total_additions": grouped["additions"].sum(),
    "total_deletions": grouped["deletions"].sum(),
    "total_changes":   grouped["changes"].sum(),
    "author_count":    grouped["author"].nunique(),
    "bug_fix_count":   all_diffs[all_diffs["is_bug_fix"] == True]
                       .groupby("filename")["date"].count(),
}).fillna(0)

# Step 4 - Calculated features
dataset["avg_changes_per_commit"] = (
    dataset["total_changes"] / dataset["commit_count"]
).round(2)

dataset["bug_fix_ratio"] = (
    dataset["bug_fix_count"] / dataset["commit_count"]
).round(2)

dataset["churn_ratio"] = (
    dataset["total_deletions"] / (dataset["total_additions"] + 1)
).round(2)

# Step 5 - Add label
dataset["has_bug"] = (dataset["bug_fix_count"] > 0).astype(int)
dataset = dataset.reset_index()

# Step 6 - Save to feature_dataset table in DB
dataset.to_sql("feature_dataset", conn, if_exists="replace", index=False)

total = pd.read_sql(
    "SELECT COUNT(*) as total FROM feature_dataset", conn
).iloc[0]["total"]

print(f"feature_dataset table saved — {total} files")
print(f"Buggy files : {int(dataset['has_bug'].sum())}")
print(f"Clean files : {int((dataset['has_bug'] == 0).sum())}")

conn.close()