import sqlite3
import numpy as np
import json
from gensim.models import KeyedVectors
from tqdm import tqdm


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


# Funcția care calculează și salvează vectorii medii pentru fiecare origin
def save_average_vectors_by_origin(keywords_and_origins, model, output_file):
    print("Se calculează vectorii medii pentru fiecare origin...")
    origin_vectors = {}

    # Calculăm vectorul mediu pentru fiecare origin
    for keyword, origin in tqdm(
        keywords_and_origins, desc="Calculare vectori medii pentru origin"
    ):
        vector = get_average_vector(keyword, model)

        # Dacă originul nu există în dicționar, îl adăugăm
        if origin not in origin_vectors:
            origin_vectors[origin] = []

        origin_vectors[origin].append(vector)

    # Calculăm media vectorilor pentru fiecare origin
    for origin in origin_vectors:
        origin_vectors[origin] = np.mean(
            origin_vectors[origin], axis=0
        ).tolist()  # Media vectorilor pentru origin

    # Salvăm vectorii medii într-un fișier JSON
    print(
        f"Se salvează vectorii medii pentru fiecare origin într-un fișier {output_file}..."
    )
    with open(output_file, "w") as f:
        json.dump(origin_vectors, f)

    print("Vectorii au fost salvați cu succes!")


if __name__ == "__main__":
    # Calea către modelul Word2Vec pre-antrenat Google News
    model_path = "gnews.bin"

    # Încarcă modelul Word2Vec
    model = load_word2vec_model(model_path)

    # Calea către baza de date SQLite
    db_path = "keywords.db"

    # Extragem keyword-urile și origin-urile din baza de date
    keywords_and_origins = fetch_keywords_from_db(db_path)

    # Calea către fișierul de ieșire (fișier JSON pentru vectori)
    output_file = "average_vectors_by_origin2.json"

    # Calculăm și salvăm vectorii medii pentru fiecare origin
    save_average_vectors_by_origin(keywords_and_origins, model, output_file)
