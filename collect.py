import requests
import pandas as pd
from datetime import datetime
from config import TOKEN

REPO = "scikit-learn/scikit-learn"
HEADERS = {"Authorization": f"token {TOKEN}"}
TODAY = datetime.now().strftime("%Y-%m-%d")

print(f"Collecting commit diffs for {TODAY}...")

# Step 1 - Get list of recent commits
commits = requests.get(
    f"https://api.github.com/repos/{REPO}/commits",
    headers=HEADERS,
    params={"per_page": 500}
).json()

file_data = []

# Step 2 - For each commit get the files changed
for commit in commits:
    sha    = commit["sha"]
    message = commit["commit"]["message"][:80]
    date   = commit["commit"]["author"]["date"]
    author = commit["commit"]["author"]["name"]

    # Check if this commit is a bug fix
    is_bug_fix = "fix" in message.lower() or "#" in message

    # Get the diff details for this commit
    detail = requests.get(
        f"https://api.github.com/repos/{REPO}/commits/{sha}",
        headers=HEADERS
    ).json()

    # Step 3 - For each file changed in this commit
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

# Step 4 - Save to CSV
pd.DataFrame(file_data).to_csv(f"data/diffs_{TODAY}.csv", index=False)
print(f"✅ Saved {len(file_data)} file changes to data/diffs_{TODAY}.csv")
