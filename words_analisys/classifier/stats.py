import sqlite3
from gensim.models import KeyedVectors


# Load the Google News Word2Vec model
def load_word2vec_model(model_path):
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    return model


# Fetch all keywords from the SQLite database
def get_keywords_from_db():
    conn = sqlite3.connect("db/keywords.db")  # Adjust the path if needed
    cursor = conn.cursor()

    # Fetch all keywords from the table
    cursor.execute("SELECT keyword FROM keywords")
    keywords = cursor.fetchall()

    conn.close()

    # Return a list of keywords
    return keywords


# Count the words in the DB, in the Word2Vec model, and in both
def count_words_in_model_and_db(db_keywords, word2vec_model):
    db_set = set(db_keywords)  # Convert DB keywords to set for faster lookup
    word2vec_vocab = set(word2vec_model.key_to_index.keys())  # Word2Vec vocabulary

    # Words in the DB and Word2Vec model
    common_words = db_set.intersection(word2vec_vocab)

    # Words in the DB but not in Word2Vec model
    db_only_words = db_set.difference(word2vec_vocab)

    # Words in Word2Vec model but not in the DB
    word2vec_only_words = word2vec_vocab.difference(db_set)
    print("First 10 words in DB only:", list(db_only_words)[:10])
    return (
        len(db_set),
        len(word2vec_vocab),
        len(common_words),
        len(db_only_words),
        len(word2vec_only_words),
    )


# Main function
def main():
    # Path to your Google News Word2Vec model file (e.g. word2vec.bin)
    model_path = "gnews.bin"  # Adjust path

    # Load the model
    print("Loading Word2Vec model...")
    word2vec_model = load_word2vec_model(model_path)

    # Fetch keywords from the database
    print("Fetching keywords from the database...")
    db_keywords = get_keywords_from_db()

    # Count words in DB, Word2Vec model, and common words
    db_count, word2vec_count, common_count, db_only_count, word2vec_only_count = (
        count_words_in_model_and_db(db_keywords, word2vec_model)
    )

    # Display results
    print(f"Total keywords in DB: {db_count}")
    print(f"Total words in Word2Vec model: {word2vec_count}")
    print(f"Common words between DB and Word2Vec model: {common_count}")
    print(f"Words in DB but not in Word2Vec model: {db_only_count}")
    print(f"Words in Word2Vec model but not in DB: {word2vec_only_count}")


# Run the script
if __name__ == "__main__":
    main()
