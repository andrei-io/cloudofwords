import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel

# Descarcă resursele necesare pentru NLTK
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


# Tokenizare, eliminare stopwords și lematizare
def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    tokens = [
        lemmatizer.lemmatize(word.lower())
        for word in tokens
        if word.isalpha() and word.lower() not in stop_words and len(word) > 2
    ]
    return tokens


def extract_lda_keywords(text, num_topics=3, passes=20, random_state=42) -> list[str]:
    """
    Extrage cuvinte cheie dintr-un document folosind LDA (Latent Dirichlet Allocation).

    Parameters:
        text (str): Textul din care vor fi extrase cuvintele cheie.
        num_topics (int): Numărul de subiecte de generat. Implicit este 3.
        passes (int): Numărul de treceri prin corpus pentru a îmbunătăți stabilitatea rezultatelor. Implicit este 20.
        random_state (int): Setează starea randomizării pentru reproductibilitate. Implicit este 42.

    Returns:
        list[str]: O listă de stringuri reprezentând cuvintele cheie extrase din toate subiectele.

    Throws:
        ValueError: Dacă textul preprocesat sau corpusul este gol.
    """

    # Aplică preprocesarea textului
    processed_text = preprocess_text(text)

    # Verificare dacă textul preprocesat este gol
    if not processed_text:
        raise ValueError(
            "Textul preprocesat este gol. Verificați conținutul textului de intrare."
        )

    # Construiește dicționarul și corpusul pentru LDA
    dictionary = Dictionary([processed_text])
    dictionary.filter_extremes(no_below=1, no_above=1.0)
    corpus = [dictionary.doc2bow(processed_text)]

    # Verificare dacă corpusul este gol
    if not corpus or len(corpus[0]) == 0:
        raise ValueError("Corpus gol după filtrare, verificați textul de intrare.")

    # Antrenează modelul LDA
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=random_state,
        passes=passes,
        alpha="auto",
        eta="auto",
    )

    # Extrage cuvintele cheie pentru fiecare temă și le combină într-o listă unică
    keywords = []
    for topic_num in range(lda_model.num_topics):
        keywords.extend(
            dictionary[idx]
            for idx, score in lda_model.show_topic(topic_num, topn=10)
            if idx in dictionary
        )

    return keywords
