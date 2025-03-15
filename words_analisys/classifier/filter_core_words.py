import sqlite3
import re
from gensim.models import KeyedVectors


# Load the Google News Word2Vec model
def load_word2vec_model(model_path):
    print("Loading Word2Vec model...")
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    print(f"Loaded Word2Vec model with {len(model.key_to_index)} words.")
    return model


# Fetch all unique (keyword, origin) pairs from the SQLite database
def get_keywords_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT keyword, origin FROM keywords")
    rows = cursor.fetchall()
    conn.close()

    print(f"Found {len(rows)} (keyword, origin) pairs in {db_path}.")

    return rows


# Filter function: Exclude keywords containing numbers
def filter_valid_words(words):
    filtered_words = [(kw, origin) for kw, origin in words if not re.search(r"\d", kw)]
    print(f"Filtered out {len(words) - len(filtered_words)} words containing numbers.")
    return filtered_words


# Create a new database and insert unique (keyword, origin) pairs
def create_final_db(filtered_words, word2vec_model, output_db_path):
    conn = sqlite3.connect(output_db_path)
    cursor = conn.cursor()

    # Drop and create the table with uniqueness constraint on (keyword, origin)
    cursor.execute("DROP TABLE IF EXISTS keywords")
    cursor.execute(
        """
        CREATE TABLE keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            origin TEXT,
            UNIQUE(keyword, origin)  -- Ensure uniqueness of (keyword, origin) pairs
        )
        """
    )

    # Convert Word2Vec vocab to a set for faster lookup
    model_vocab = set(word2vec_model.key_to_index.keys())

    # Filter out words that are not in Word2Vec model
    words_to_insert = [
        (kw, origin) for kw, origin in filtered_words if kw not in model_vocab
    ]

    print(
        f"Filtered out {len(filtered_words) - len(words_to_insert)} words found in Word2Vec model."
    )
    print(f"Remaining words to insert: {len(words_to_insert)}")

    # Insert words into final_unique.db with UNIQUE constraint on (keyword, origin)
    cursor.executemany(
        "INSERT OR IGNORE INTO keywords (keyword, origin) VALUES (?, ?)",
        words_to_insert,
    )

    conn.commit()
    conn.close()

    print(
        f"Inserted {len(words_to_insert)} unique (keyword, origin) pairs into {output_db_path}."
    )

    return len(words_to_insert)


# Main function
def main():
    model_path = "gnews.bin"  # Update with correct path
    input_db_path = "db/keywords.db"
    output_db_path = "db/final_unique.db"

    word2vec_model = load_word2vec_model(model_path)
    keyword_list = get_keywords_from_db(input_db_path)

    print(f"Total words before filtering: {len(keyword_list)}")

    filtered_words = filter_valid_words(keyword_list)

    print(f"Total words after removing numbers: {len(filtered_words)}")

    total_inserted = create_final_db(filtered_words, word2vec_model, output_db_path)

    print("\nProcess Complete!")
    print(f"Total words before filtering: {len(keyword_list)}")
    print(
        f"Words removed (contained numbers): {len(keyword_list) - len(filtered_words)}"
    )
    print(f"Words missing from Word2Vec model: {total_inserted}")
    print(
        f"Total unique (keyword, origin) pairs inserted into final_unique.db: {total_inserted}"
    )


# Run the script
if __name__ == "__main__":
    main()
