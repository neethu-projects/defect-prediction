import requests
import pandas as pd
from config import TOKEN


REPO  = "scikit-learn/scikit-learn"
HEADERS = {"Authorization": f"token {TOKEN}"}

# Get 5 bug issues from GitHub
issues = requests.get(
    f"https://api.github.com/repos/{REPO}/issues",
    headers=HEADERS,
    params={"labels": "Bug", "per_page": 5}
).json()

# Print only the important fields
for issue in issues:
    print(issue["number"], issue["title"])

# Save to CSV
pd.DataFrame(issues).to_csv("test_issues.csv", index=False)
print("✅ Saved to test_issues.csv")
