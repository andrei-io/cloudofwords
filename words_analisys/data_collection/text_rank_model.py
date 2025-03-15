import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import networkx as nx

# Descarcă resursele necesare pentru NLTK
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")


def extract_textrank_keywords(text: str, top_n: int = 10) -> list[str]:
    """
    Extrage cuvinte cheie folosing algoritmul TextRank.

    Parameters:
        text (str): The input text from which to extract keywords.
        top_n (int): The number of top keywords to return.

    Returns:
        List[str]: A list of keywords ordered by their importance.
    """
    # Preprocesarea textului
    if not text:
        raise ValueError(
            "Textul preprocesat este gol. Verificați conținutul textului de intrare."
        )
    # Tokenize sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Înlăturarea stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [
        word for word in words if word.isalnum() and word not in stop_words
    ]

    # Crearea unui grafic bazat pe cuvinte
    graph = nx.Graph()

    # Adăugăm cuvintele ca noduri
    for word in filtered_words:
        graph.add_node(word)

    # Adăugăm muchii între cuvinte în funcție de aparițiile lor în propoziții
    for sentence in sentences:
        sentence_words = [
            word for word in word_tokenize(sentence.lower()) if word in graph
        ]
        for i in range(len(sentence_words)):
            for j in range(i + 1, len(sentence_words)):
                if graph.has_edge(sentence_words[i], sentence_words[j]):
                    graph[sentence_words[i]][sentence_words[j]]["weight"] += 1
                else:
                    graph.add_edge(sentence_words[i], sentence_words[j], weight=1)

    # Calcularea scorurilor TextRank
    scores = nx.pagerank(graph)

    # Obținerea celor mai importante cuvinte
    keywords = Counter(scores).most_common(top_n)

    # Verifică dacă există suficiente cuvinte cheie, și dacă nu, ajustează top_n
    top_n = min(top_n, len(keywords))

    # Returnează cuvintele cheie extrase
    return [keywords[i][0] for i in range(top_n)]
