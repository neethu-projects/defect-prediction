import pandas as pd
import sqlite3
import glob
import os

print("Loading all CSV files into database...")

# CONNECT TO DATABASE 
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/defect_data.db")

# LOAD ALL CSV FILES 
csv_files = glob.glob("data/diffs_*.csv")

if not csv_files:
    print("No CSV files found in data/ folder")
else:
    total_rows = 0

    for file in csv_files:
        df = pd.read_csv(file)
        df.to_sql("diffs", conn, if_exists="append", index=False)
        total_rows += len(df)
        print(f"Loaded {file} — {len(df)} rows")

    # REMOVE DUPLICATES FROM DATABASE
    print("\nRemoving duplicates...")
    conn.execute("""
        DELETE FROM diffs
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM diffs
            GROUP BY filename, date, author
        )
    """)
    conn.commit()

    # SHOW FINAL COUNT
    total = pd.read_sql("SELECT COUNT(*) as total FROM diffs", conn).iloc[0]["total"]
    print(f"\n--- Summary ---")
    print(f"CSV files loaded : {len(csv_files)}")
    print(f"Rows inserted    : {total_rows}")
    print(f"Rows in database : {total}")
    print(f"All data loaded to data/defect_data.db")

conn.close()