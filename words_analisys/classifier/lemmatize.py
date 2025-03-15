import sqlite3
import spacy


# Load the spaCy English model for lemmatization
def load_spacy_model():
    nlp = spacy.load("en_core_web_sm")
    return nlp


# Fetch all keywords from the final.db SQLite database
def get_keywords_from_final_db():
    conn = sqlite3.connect("db/final.db")  # Adjust path if needed
    cursor = conn.cursor()

    # Fetch all keywords from the table
    cursor.execute("SELECT id, keyword FROM keywords")
    keywords = cursor.fetchall()

    conn.close()

    # Return a list of tuples (id, keyword)
    return keywords


# Lemmatize each word and update the database with the lemmatized word
def lemmatize_words_in_db(keywords, nlp_model):
    conn = sqlite3.connect("db/final.db")
    cursor = conn.cursor()

    # Prepare the list of updates (id, lemmatized keyword)
    lemmatized_keywords = []

    for keyword in keywords:
        doc = nlp_model(keyword[1])  # Process the word with spaCy
        lemmatized_word = doc[
            0
        ].lemma_  # Lemmatize the word (get the first token lemma)

        # Add the id and lemmatized keyword to the list
        lemmatized_keywords.append((lemmatized_word, keyword[0]))

    # Update the database with the lemmatized words
    cursor.executemany(
        "UPDATE keywords SET keyword = ? WHERE id = ?", lemmatized_keywords
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Lemmatized {len(lemmatized_keywords)} words.")


# Main function
def main():
    # Load the spaCy model
    print("Loading spaCy model for lemmatization...")
    nlp_model = load_spacy_model()

    # Fetch all keywords from the final.db
    print("Fetching keywords from final.db...")
    keywords = get_keywords_from_final_db()

    # Lemmatize words and update the database
    print("Lemmatizing words in the database...")
    lemmatize_words_in_db(keywords, nlp_model)


# Run the script
if __name__ == "__main__":
    main()
