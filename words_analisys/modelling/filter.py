import sqlite3
import numpy as np
import spacy
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm  # Biblioteca tqdm pentru progres
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")


# Încarcă modelul Word2Vec pre-antrenat de la Google News
def load_word2vec_model(model_path):
    print(f"Se incarca modelul de la {model_path}...")
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    print("Modelul a fost incarcat cu succes!")
    return model


# Funcție pentru a calcula vectorul mediu al unui text
def get_average_vector(text, model):
    tokens = text.split()  # presupunem că textul e deja tokenizat
    vectors = []
    for word in tokens:
        if word in model:
            vectors.append(model[word])
    if vectors:
        return np.mean(vectors, axis=0)  # media vectorilor cuvintelor
    else:
        return np.zeros(model.vector_size)  # daca niciun cuvant nu e in vocabular


# Funcție pentru a calcula similaritatea cosinus între doi vectori
def calculate_cosine_similarity(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]


# Preprocesare: tokenizare și lemmatizare
def preprocess_text(text: str) -> str:
    """
    Preprocesses the input text by performing tokenization and lemmatization.

    Parameters:
        text (str): The input text to be processed.

    Returns:
        str: A string of lemmatized words after tokenization and stopword removal.
    """
    if not text:
        raise ValueError("Textul de intrare este gol.")

    # Stopwords = cuvinte de umplutura
    stop_words = set(
        stopwords.words("english")
    )  # Cuvinte de umplutura in limba engleza

    # Încarcă procesorul spaCy pentru limba engleză
    nlp_processor = spacy.load(
        "en_core_web_sm"
    )  # Asigură-te că ai modelul spaCy corect
    doc = nlp_processor(
        text.lower()
    )  # Procesează textul și îl convertește în litere mici

    # Lematizare și eliminare stopwords
    lemmatized_tokens = [
        token.lemma_
        for token in doc
        if token.is_alpha and token.lemma_ not in stop_words
    ]

    return " ".join(lemmatized_tokens)


# Conectare la baza de date SQLite și extragerea keyword-urilor și origin-urilor
def fetch_keywords_from_db(db_path):
    print("Se extrag keyword-urile din baza de date...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Executăm interogarea pentru a obține keyword și origin
    cursor.execute("SELECT keyword, origin FROM keywords")
    rows = cursor.fetchall()

    # Închidem conexiunea la baza de date
    conn.close()

    print(f"Am extras {len(rows)} keyword-uri din baza de date.")
    return rows


# Funcția principală care va compara fraza utilizatorului cu keyword-urile din baza de date
def find_most_similar_origin(user_input, keywords_and_origins, model):
    print("Se calculează vectorul frazei utilizatorului...")
    # Preprocesăm fraza utilizatorului
    user_input_processed = preprocess_text(user_input)
    user_vector = get_average_vector(user_input_processed, model)

    # Calculăm vectorii pentru fiecare keyword din baza de date
    print("Se calculează vectorii pentru fiecare keyword din baza de date...")
    keyword_vectors = []
    for keyword, _ in tqdm(
        keywords_and_origins, desc="Calculare vectori pentru keyword-uri"
    ):
        keyword_processed = preprocess_text(keyword)
        keyword_vectors.append(get_average_vector(keyword_processed, model))

    # Calculăm similaritatea cosinus între fraza utilizatorului și fiecare keyword
    print("Se calculează similaritatea cosinus pentru fiecare keyword...")
    similarities = []
    for keyword_vector in tqdm(keyword_vectors, desc="Calculare similaritate cosinus"):
        similarities.append(calculate_cosine_similarity(user_vector, keyword_vector))

    # Găsim indexul celui mai apropiat keyword și origin-ul asociat
    most_similar_index = np.argmax(similarities)
    most_similar_origin = keywords_and_origins[most_similar_index][
        1
    ]  # Eticheta origin asociată

    return most_similar_origin, similarities[most_similar_index]


if __name__ == "__main__":
    # Calea către modelul Word2Vec pre-antrenat Google News
    model_path = "path_to_your_downloaded_model/GoogleNews-vectors-negative300.bin"

    # Încarcăm modelul Word2Vec
    print("Încărc modelul Word2Vec...")
    model = load_word2vec_model(model_path)

    # Calea către baza de date SQLite
    db_path = "filtered_keywords.db"

    # Extragem keyword-urile și origin-urile din baza de date
    keywords_and_origins = fetch_keywords_from_db(db_path)

    # Fraza introdusă de utilizator
    user_input = "acesta este un exemplu de text"

    # Căutăm eticheta origin cea mai apropiată de fraza utilizatorului
    print("Se caută eticheta origin cea mai apropiată frazei utilizatorului...")
    most_similar_origin, similarity_score = find_most_similar_origin(
        user_input, keywords_and_origins, model
    )

    # Afișăm rezultatul
    print(
        f"Eticheta cea mai apropiată: {most_similar_origin} (similaritate: {similarity_score:.4f})"
    )
