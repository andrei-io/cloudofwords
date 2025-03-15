import sqlite3
import nltk
import numpy as np
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import spacy
from tqdm import tqdm  # Biblioteca tqdm pentru progres
import json

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


# Funcție pentru a încărca vectorii medii salvați pentru fiecare origin
def load_average_vectors_by_origin(input_file):
    print(
        f"Se încarcă vectorii medii pentru fiecare origin din fișierul {input_file}..."
    )
    with open(input_file, "r") as f:
        origin_vectors = json.load(f)
    print(f"Vectorii au fost încărcați cu succes din {input_file}.")
    return origin_vectors


def calculate_cosine_similarity(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]


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


def preprocess_text(text):
    nlp = spacy.load("en_core_web_sm")
    stop_words = set(stopwords.words("english"))

    # Preprocesăm textul cu spaCy
    doc = nlp(text.lower())  # Convertem textul la litere mici
    tokens = [
        token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha
    ]  # Lematizăm și eliminăm stopwords și non-alfabetice

    return " ".join(tokens)


# Funcția principală care va compara fraza utilizatorului cu origin-urile
def find_most_similar_origin(user_input, origin_vectors, keywords_and_origins, model):
    print("Se calculează vectorul frazei utilizatorului...")
    # Preprocesăm fraza utilizatorului
    user_input_processed = preprocess_text(
        user_input
    )  # Preprocesăm textul (dacă este necesar)
    user_vector = get_average_vector(user_input_processed, model)

    # Calculăm similaritatea cosinus între fraza utilizatorului și fiecare origin
    print("Se calculează similaritatea cosinus pentru fiecare origin...")
    similarities = []
    for origin in tqdm(origin_vectors, desc="Calculare similaritate cosinus"):
        origin_vector = origin_vectors[origin]

        similarities.append(calculate_cosine_similarity(user_vector, origin_vector))

    # Găsim origin-ul cel mai apropiat și returnăm
    most_similar_origin = list(origin_vectors.keys())[np.argmax(similarities)]
    return most_similar_origin, similarities[np.argmax(similarities)]


if __name__ == "__main__":
    # Calea către modelul Word2Vec pre-antrenat Google News
    model_path = "gnews.bin"

    # Încarcă modelul Word2Vec
    model = load_word2vec_model(model_path)

    # Calea către fișierul cu vectorii medii salvați pentru fiecare origin
    input_file = "average_vectors_by_origin2.json"

    # Încarcă vectorii medii salvați
    origin_vectors = load_average_vectors_by_origin(input_file)

    # Calea către baza de date SQLite
    db_path = "filtered_keywords.db"

    # Extragem keyword-urile și origin-urile din baza de date
    keywords_and_origins = fetch_keywords_from_db(db_path)

    # Fraza introdusă de utilizator
    user_input = "The digitalization of data has resulted in a data tsunami in practically every industry of data-driven enterprise. Furthermore, man-to-machine (M2M) digital data handling has dramatically amplified the information wave. There has been a significant development in digital agriculture management applications, which has impacted information and communication technology (ICT) to deliver benefits for both farmers and consumers, as well as pushed technological solutions into rural settings. This paper highlights the potential of ICT technologies in traditional agriculture, as well as the challenges that may arise when they are used in farming techniques. Robotics, Internet of things (IoT) devices, and machine learning issues, as well as the functions of machine learning, artificial intelligence, and sensors in agriculture, are all detailed. In addition, drones are being considered for crop observation as well as crop yield optimization management. When applicable, worldwide and cutting-edge IoT-based farming systems and platforms are also highlighted. We do a thorough review of the most recent literature in each area of expertise. We conclude the present and future trends in artificial intelligence (AI) and highlight existing and emerging research problems in AI in agriculture due to this comprehensive assessment."

    # Căutăm eticheta origin cea mai apropiată de fraza utilizatorului
    print("Se caută eticheta origin cea mai apropiată frazei utilizatorului...")
    most_similar_origin, similarity_score = find_most_similar_origin(
        user_input, origin_vectors, keywords_and_origins, model
    )

    # Afișăm rezultatul
    print(
        f"Eticheta cea mai apropiată: {most_similar_origin} (similaritate: {similarity_score:.4f})"
    )
