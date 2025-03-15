import psycopg2
from gensim.models import KeyedVectors

# Database connection details
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "mysecretpassword"
DB_HOST = "localhost"  # Change to "cloudofwords" if connecting via Docker network
DB_PORT = "5432"

# Path to GoogleNews word2vec model
MODEL_PATH = "gnews.bin"


def load_model(model_path):
    print("Loading Word2Vec model...")
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    print("Model loaded successfully.")
    return model


def insert_keywords(words):
    """Inserts words into the gnews table in PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()

        # Prepare the insert query
        insert_query = "INSERT INTO gnews (keyword) VALUES (%s) ON CONFLICT DO NOTHING"

        # Insert words in batches for efficiency
        batch_size = 1000
        word_list = list(words)
        for i in range(0, len(word_list), batch_size):
            batch = [(word,) for word in word_list[i : i + batch_size]]
            cur.executemany(insert_query, batch)
            conn.commit()
            print(f"Inserted {i + len(batch)} words...")

        cur.close()
        conn.close()
        print("All words inserted successfully.")

    except Exception as e:
        print(f"Database error: {e}")


if __name__ == "__main__":
    model = load_model(MODEL_PATH)
    insert_keywords(model.key_to_index.keys())  # Extract words from model
