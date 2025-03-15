import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from typing import List

nltk.download("stopwords")


def extract_tfidf_keywords(text: str) -> list[str]:
    """
    Extracts keywords from the input text using TF-IDF (Term Frequency - Inverse Document Frequency).

    Parameters:
        text (str): The input text from which to extract keywords.

    Returns:
        List[str]: A list of words ordered by their relevance (importance).
    """
    if not text:
        raise ValueError(
            "Textul preprocesat este gol. Verificați conținutul textului de intrare."
        )

    # Stopwords = cuvinte de umplutura
    stop_words = list(stopwords.words("english"))  # Convertește în listă

    # 1. Preprocesare
    nlp_processor = spacy.load(
        "en_core_web_sm"
    )  # Încarcă procesorul spaCy pentru limba engleză
    doc = nlp_processor(
        text.lower()
    )  # Procesează textul și îl convertește în litere mici

    # 2. Lematizare și eliminarea stopwords
    filtered_text = " ".join(
        [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    )

    # 3. Calculul frecvenței cuvintelor prin TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words=stop_words
    )  # `stop_words` este acum o listă
    X = vectorizer.fit_transform([filtered_text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = X.toarray()[0]

    # 4. Sortăm cuvintele după relevanță
    important_words = sorted(
        zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True
    )

    # Extragem doar cuvintele într-un vector de stringuri
    word_vector = [word for word, score in important_words if score > 0]

    return word_vector
