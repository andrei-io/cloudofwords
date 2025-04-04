import sqlite3

# Database paths
INPUT_DB_PATH = "../db/textrank_keywords.db"
OUTPUT_DB_PATH = "../db/textrank_unique.db"


# Load all unique (keyword, origin) pairs from keywords.db
def load_unique_keywords(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT keyword, origin FROM keywords")
    words = {row for row in cursor.fetchall()}  # Set to remove exact duplicates

    conn.close()
    print(f"Loaded {len(words)} unique (keyword, origin) pairs from {db_path}.")
    return words


# Filter out words containing numbers while keeping origin
def filter_valid_words(words):
    filtered_words = {row for row in words if not any(c.isdigit() for c in row[0])}
    print(f"Filtered out {len(words) - len(filtered_words)} words containing numbers.")
    return filtered_words


# Save unique (keyword, origin) pairs to the new database
def save_unique_words(db_path, unique_words):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop existing table
    cursor.execute("DROP TABLE IF EXISTS keywords")

    # Recreate table without UNIQUE constraint on keyword
    cursor.execute(
        """
        CREATE TABLE keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            origin TEXT,
            UNIQUE(keyword, origin) 
        )
        """
    )

    # Insert words
    cursor.executemany(
        "INSERT OR IGNORE INTO keywords (keyword, origin) VALUES (?, ?)", unique_words
    )

    conn.commit()
    total_inserted = cursor.execute("SELECT COUNT(*) FROM keywords").fetchone()[0]
    conn.close()

    print(f"Inserted {total_inserted} unique (keyword, origin) pairs into {db_path}.")
    return total_inserted


# Main function
def main():
    unique_words = load_unique_keywords(INPUT_DB_PATH)
    print(f"Total words before filtering: {len(unique_words)}")

    filtered_words = filter_valid_words(unique_words)

    print(f"Total words after removing numbers: {len(filtered_words)}")

    total_inserted = save_unique_words(OUTPUT_DB_PATH, filtered_words)

    print(f"\nProcess completed successfully!")
    print(
        f"Final count of unique (keyword, origin) pairs in {OUTPUT_DB_PATH}: {total_inserted}"
    )


# Run the script
if __name__ == "__main__":
    main()
