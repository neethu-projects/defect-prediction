# Defect Prediction from Commit Diffs

## Project Overview
This project builds a defect prediction model using commit diff history
from popular open source Python repositories on GitHub. The goal is to
predict which files in a codebase are most likely to contain bugs based
on their change history.

## SQA Concept
Predictive Quality Analytics — using historical data to identify
high-risk files before bugs are reported, helping QA teams prioritise
their testing effort.

## Data Source
Data is collected from the following GitHub repositories via the
GitHub REST API:
- scikit-learn/scikit-learn

## How It Works

### Step 1 - Data Collection (collect.py)
Calls the GitHub API and collects commit diffs daily.
For each commit records which files changed, how many lines
were added and deleted, and whether the commit was a bug fix.
Saves raw data to the raw_diffs table in the database.

### Step 2 - Feature Extraction (features.py)
Reads all raw data from the database and calculates 9 features
per file:

| Feature | Description |
|---|---|
| commit_count | How many times the file was changed |
| total_additions | Total lines added across all commits |
| total_deletions | Total lines deleted across all commits |
| total_changes | Total lines changed across all commits |
| author_count | How many different developers touched it |
| bug_fix_count | How many bug fixing commits touched it |
| avg_changes_per_commit | Average size of each change |
| bug_fix_ratio | Percentage of commits that were bug fixes |
| churn_ratio | Ratio of deletions to additions |
| has_bug | Label — 1 if buggy, 0 if clean |

Saves the feature table to the feature_dataset table in the database.

### Step 3 - Testing (tests.py)
Runs unit tests on the bug fix detection logic and integration
tests on the database to verify data quality and pipeline integrity.

## Database Schema

### Table 1 — raw_diffs
| Column | Description |
|---|---|
| filename | Path of the file changed |
| additions | Lines added in this commit |
| deletions | Lines deleted in this commit |
| changes | Total lines changed |
| is_bug_fix | True if commit was a bug fix |
| author | Developer who made the commit |
| date | Date of the commit |


### Table 2 — feature_dataset
| Column | Description |
|---|---|
| filename | Path of the file |
| commit_count | Total commits touching this file |
| total_additions | Total lines added |
| total_deletions | Total lines deleted |
| total_changes | Total lines changed |
| author_count | Unique authors |
| bug_fix_count | Bug fix commits |
| avg_changes_per_commit | Average change size |
| bug_fix_ratio | Bug fix percentage |
| churn_ratio | Deletion to addition ratio |
| has_bug | 1 = buggy, 0 = clean |

## How to Run

### Install dependencies
pip install requests pandas

### Collect data daily
python collect.py

### Extract features
python features.py

### Run tests
python tests.py

## Requirements
requests
pandas
scikit-learn
matplotlib

## Data Ethics
All data is collected from public open source repositories
using the official GitHub REST API within the free tier rate
limits of 5000 requests per hour. No private repositories
or personal user data is collected.

## AI Usage Attribution
This project was developed with assistance from Claude AI
(Anthropic) for code guidance, debugging, and documentation.


## Author
Neethu Sreekumar (20092130)
MSc Artificial Intelligence
Module: B9AI001 Programming for Data Analysis
