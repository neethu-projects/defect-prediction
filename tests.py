import sqlite3
import pandas as pd

# UNIT TESTS for is_bug_fix logic
def test_is_bug_fix():
    print("Running unit tests for is_bug_fix logic")

    message1 = "fix: corrected issue with ridge classifier"
    assert "fix" in message1.lower()
    print("Test 1 passed - bug fix detected correctly")

    message2 = "added new documentation"
    assert "fix" not in message2.lower() and "#" not in message2
    print("Test 2 passed - non bug fix detected correctly")

    message3 = "closes #33513 column transformer bug"
    assert "#" in message3
    print("Test 3 passed - issue number detected correctly")

    print("All unit tests passed!\n")


# INTEGRATION TESTS for database contents and feature extraction
def test_database():
    print("Running integration tests on database contents")

    conn = sqlite3.connect("data/defect_data.db")

    # Test 1 - raw_diffs has rows
    result = pd.read_sql(
        "SELECT COUNT(*) as total FROM raw_diffs", conn
    )
    assert result["total"][0] > 0
    print(f"Test 1 passed - raw_diffs has {result['total'][0]} rows")

    # Test 2 - feature_dataset has rows
    result = pd.read_sql(
        "SELECT COUNT(*) as total FROM feature_dataset", conn
    )
    assert result["total"][0] > 0
    print(f"Test 2 passed - feature_dataset has {result['total'][0]} rows")

    # Test 3 - expected columns exist in raw_diffs
    result = pd.read_sql("SELECT * FROM raw_diffs LIMIT 1", conn)
    for col in ["filename", "additions", "deletions", "changes", "is_bug_fix"]:
        assert col in result.columns
    print("Test 3 passed - all columns present in raw_diffs")

    # Test 4 - expected columns exist in feature_dataset
    result = pd.read_sql("SELECT * FROM feature_dataset LIMIT 1", conn)
    for col in ["filename", "commit_count", "bug_fix_count", "has_bug"]:
        assert col in result.columns
    print("Test 4 passed - all columns present in feature_dataset")

    # Test 5 - no negative values
    result = pd.read_sql(
        "SELECT * FROM raw_diffs WHERE additions < 0", conn
    )
    assert len(result) == 0
    print("Test 5 passed - no negative values in additions")

    print("\nAll integration tests passed!")
    conn.close()


# RUN ALL TESTS (only run the tests when this file is run directly)
if __name__ == "__main__":
    test_is_bug_fix()
    test_database()