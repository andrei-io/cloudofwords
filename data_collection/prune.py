import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")

db_file_out = "refined.db"

# Connect to the database
conn_input = sqlite3.connect("/home/oni/dev/Working/cloudofwords/keywords.db")
conn_output = sqlite3.connect(db_file_out)

cursor_out = conn_output.cursor()
# Create table if it doesn't exist
cursor_out.execute(
    """
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    origin TEXT,
    score REAL
)
"""
)

cursor = conn_input.cursor()

# Query to get words grouped by source
query = (
    "SELECT origin, GROUP_CONCAT(keyword, ' ') as words FROM keywords GROUP BY origin"
)
cursor.execute(query)

# Fetch all results
data = cursor.fetchall()

# Close the connection
conn_input.close()

# Prepare data for TF-IDF
sources = [row[0] for row in data]
documents = [row[1] for row in data]

# Load spaCy model and stopwords
nlp_processor = spacy.load("en_core_web_sm")
stop_words = list(stopwords.words("english"))

# Preprocess documents
preprocessed_documents = []
for doc in documents:
    # increase max length
    nlp_processor.max_length = 2610392
    spacy_doc = nlp_processor(doc.lower())
    filtered_text = " ".join(
        [token.lemma_ for token in spacy_doc if not token.is_stop and token.is_alpha]
    )
    preprocessed_documents.append(filtered_text)

# Run TF-IDF
vectorizer = TfidfVectorizer(stop_words=stop_words)
tfidf_matrix = vectorizer.fit_transform(preprocessed_documents)

# Print the TF-IDF scores
feature_names = vectorizer.get_feature_names_out()
for i, source in enumerate(sources):
    print(f"Source: {source}")
    for j in range(len(feature_names)):
        if tfidf_matrix[i, j] > 0:
            print(f"{feature_names[j]}: {tfidf_matrix[i, j]}")
            cursor_out.execute(
                "INSERT INTO keywords (keyword, origin, score) VALUES (?, ?, ?)",
                (feature_names[j], source, tfidf_matrix[i, j]),
            )
    print("\n")

conn_output.commit()
conn_output.close()
