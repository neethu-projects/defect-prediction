import requests
import pandas as pd
from datetime import datetime, timedelta
from config import TOKEN

REPO = "scikit-learn/scikit-learn"
HEADERS = {"Authorization": f"token {TOKEN}"}
TODAY = datetime.now().strftime("%Y-%m-%d")

# Go back 60 days to get enough data
SINCE = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%dT%H:%M:%SZ")

print(f"Collecting commit diffs since 180 days ago...")

file_data = []
page = 1

while True:
    commits = requests.get(
        f"https://api.github.com/repos/{REPO}/commits",
        headers=HEADERS,
        params={"per_page": 100, "since": SINCE, "page": page}
    ).json()

    # Stop if no more commits
    if not commits or not isinstance(commits, list):
        break

    print(f"Processing page {page} — {len(commits)} commits...")

    for commit in commits:
        sha     = commit["sha"]
        message = commit["commit"]["message"][:80]
        date    = commit["commit"]["author"]["date"]
        author  = commit["commit"]["author"]["name"]

        is_bug_fix = "fix" in message.lower() or "#" in message

        detail = requests.get(
            f"https://api.github.com/repos/{REPO}/commits/{sha}",
            headers=HEADERS
        ).json()

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

    page += 1

    # Stop after 15 pages (1500 commits) to stay safe
    if page > 15:
        break

# Save to CSV
pd.DataFrame(file_data).to_csv("data/diffs_historical.csv", index=False)
print(f"\n✅ Saved {len(file_data)} file changes to data/diffs_historical.csv")
