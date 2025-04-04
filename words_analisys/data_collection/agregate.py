import os
import pandas as pd
import sqlite3

# Directory containing the Excel files
excel_dir = "../../output"

# SQLite database file
db_file = "../db/textrank_keywords.db"

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    origin TEXT
)
"""
)

# Check all files and subfolders for execel files
for root, dirs, files in os.walk(excel_dir):
    print(f"Processing {root}")
    for file in files:
        if file.endswith(".xlsx"):
            print(f"Processing {file}")
            df = pd.read_excel(os.path.join(root, file))
            for index, row in df.iterrows():
                origin = file.split("_")[0].lower()
                keywords = row["TextRank_Keywords"]
                if pd.isna(keywords) or keywords == "":
                    continue
                if len(keywords.split(", ")) < 3:
                    continue
                for keyword in keywords.split(", "):
                    cursor.execute(
                        "INSERT INTO keywords (keyword, origin) VALUES (?, ?)",
                        (keyword, origin),
                    )

# Commit changes and close connection
conn.commit()
conn.close()
