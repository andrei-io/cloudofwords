import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from collections import Counter
import networkx as nx
import numpy as np

# Descarcă resursele necesare pentru NLTK
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")


# Funcția de preprocesare
def preprocess_text(text):
    # Tokenizare
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Înlăturare stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word.isalnum() and word not in stop_words]

    return sentences, words


# Funcția de extragere a cuvintelor cheie folosind TextRank
def textrank(sentences, words, top_n=10):
    # Crearea unui grafic bazat pe cuvinte
    graph = nx.Graph()

    # Adăugăm cuvintele ca noduri
    for word in words:
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

    return keywords


# Exemplu de text
text = """
The digitalization of data has resulted in a data tsunami in practically every industry of data-driven enterprise. Furthermore, man-to-machine (M2M) digital data handling has dramatically amplified the information wave. There has been a significant development in digital agriculture management applications, which has impacted information and communication technology (ICT) to deliver benefits for both farmers and consumers, as well as pushed technological solutions into rural settings. This paper highlights the potential of ICT technologies in traditional agriculture, as well as the challenges that may arise when they are used in farming techniques.
"""

# Aplică preprocesarea textului
sentences, words = preprocess_text(text)

# Extragerea cuvintelor cheie folosind TextRank
keywords = textrank(sentences, words)

# Afișarea cuvintelor cheie
print("Cuvinte cheie extrase:", [word for word, score in keywords])
