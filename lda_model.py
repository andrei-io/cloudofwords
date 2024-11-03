# TODO: trebuie rulat pe documentul full, nu pe rezumate
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


# Preprocesare text
def preprocess_text(text):
    # Tokenizare
    tokens = word_tokenize(text)
    # Înlăturare de stopwords și lematizare
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    tokens = [
        lemmatizer.lemmatize(word.lower())  # Convertim cuvintele la litere mici
        for word in tokens
        if word.isalpha() and word.lower() not in stop_words and len(word) > 2
    ]
    return tokens


# Exemplu de text (un singur document)
text = """
The digitalization of data has resulted in a data tsunami in practically every industry of data-driven enterprise. Furthermore, man-to-machine (M2M) digital data handling has dramatically amplified the information wave. There has been a significant development in digital agriculture management applications, which has impacted information and communication technology (ICT) to deliver benefits for both farmers and consumers, as well as pushed technological solutions into rural settings. This paper highlights the potential of ICT technologies in traditional agriculture, as well as the challenges that may arise when they are used in farming techniques. Robotics, Internet of things (IoT) devices, and machine learning issues, as well as the functions of machine learning, artificial intelligence, and sensors in agriculture, are all detailed. In addition, drones are being considered for crop observation as well as crop yield optimization management. When applicable, worldwide and cutting-edge IoT-based farming systems and platforms are also highlighted. We do a thorough review of the most recent literature in each area of expertise. We conclude the present and future trends in artificial intelligence (AI) and highlight existing and emerging research problems in AI in agriculture due to this comprehensive assessment.
"""

# Aplică preprocesarea textului
processed_text = preprocess_text(text)
print("Text preprocesat:", processed_text)

# Construiește un dicționar și un corpus pentru LDA
dictionary = Dictionary([processed_text])
print("Termeni în dicționar înainte de filtrare:", dictionary.token2id)

# Elimină extremitățile (ajustat pentru un singur document)
dictionary.filter_extremes(
    no_below=1, no_above=1.0
)  # Ajustat pentru a nu elimina cuvinte
corpus = [dictionary.doc2bow(processed_text)]

# Verificare dacă corpusul este gol
if not corpus or len(corpus[0]) == 0:
    raise ValueError("Corpus gol după filtrare, verificați textul de intrare.")

# Aplică LDA pe corpus
lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=3,  # Numărul de subiecte poate fi ajustat
    random_state=42,
    passes=20,
    # iterations=50,
    alpha="auto",
    eta="auto",
)

# Extrage cuvintele cheie pentru fiecare temă
for topic_num in range(lda_model.num_topics):
    # Modificare: Verificăm ID-urile să fie în dicționar
    keywords = [
        dictionary[idx]
        for idx, score in lda_model.show_topic(topic_num, topn=10)
        if idx in dictionary
    ]
    print(f"Tema {topic_num + 1}: {keywords}")
