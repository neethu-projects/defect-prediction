import requests
import pandas as pd
from datetime import datetime
from config import TOKEN
import sqlite3
import os

REPO    = "scikit-learn/scikit-learn"
HEADERS = {"Authorization": f"token {TOKEN}"}
TODAY   = datetime.now().strftime("%Y-%m-%d")

os.makedirs("data", exist_ok=True)

print(f"Collecting commit diffs for {TODAY}...")

# Step 1 - Get recent commits (max 100 per page)
commits = requests.get(
    f"https://api.github.com/repos/{REPO}/commits",
    headers=HEADERS,
    params={"per_page": 30}
).json()

file_data = []

# Step 2 - For each commit get the files changed
for commit in commits:
    sha     = commit["sha"]
    message = commit["commit"]["message"][:80]
    date    = commit["commit"]["author"]["date"]
    author  = commit["commit"]["author"]["name"]

    # Check if this commit is a bug fix
    is_bug_fix = "fix" in message.lower() or "#" in message

    # Get the diff details for this commit
    detail = requests.get(
        f"https://api.github.com/repos/{REPO}/commits/{sha}",
        headers=HEADERS
    ).json()

    # Step 3 - For each Python file changed in this commit
    if "files" in detail:
        for file in detail["files"]:
            if file["filename"].endswith(".py"):
                file_data.append({
                    "filename":   file["filename"],
                    "additions":  file["additions"],
                    "deletions":  file["deletions"],
                    "changes":    file["changes"],
                    "is_bug_fix": is_bug_fix,
                    "author":     author,
                    "date":       date
                })

# Step 4 - Save to database
conn = sqlite3.connect("data/defect_data.db")
df = pd.DataFrame(file_data)
df.to_sql("raw_diffs", conn, if_exists="append", index=False)

# Step 5 - Remove duplicates
conn.execute("""
    DELETE FROM raw_diffs
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM raw_diffs
        GROUP BY filename, date, author
    )
""")
conn.commit()

# Step 6 - Show total count
total = pd.read_sql(
    "SELECT COUNT(*) as total FROM raw_diffs", conn
).iloc[0]["total"]

conn.close()

print(f"Saved {len(file_data)} rows to raw_diffs table")
print(f"Total rows in database: {total}")