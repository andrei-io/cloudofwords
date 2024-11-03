import nltk
import spacy
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

nltk.download("stopwords")

# Text de analizat
text = """
    The digitalization of data has resulted in a data tsunami in practically every industry of data-driven enterprise. Furthermore, man-to-machine (M2M) digital data handling has dramatically amplified the information wave. There has been a significant development in digital agriculture management applications, which has impacted information and communication technology (ICT) to deliver benefits for both farmers and consumers, as well as pushed technological solutions into rural settings. This paper highlights the potential of ICT technologies in traditional agriculture, as well as the challenges that may arise when they are used in farming techniques. Robotics, Internet of things (IoT) devices, and machine learning issues, as well as the functions of machine learning, artificial intelligence, and sensors in agriculture, are all detailed. In addition, drones are being considered for crop observation as well as crop yield optimization management. When applicable, worldwide and cutting-edge IoT-based farming systems and platforms are also highlighted. We do a thorough review of the most recent literature in each area of expertise. We conclude the present and future trends in artificial intelligence (AI) and highlight existing and emerging research problems in AI in agriculture due to this comprehensive assessment.
"""

# Stopwords = cuvinte de umplutura
stop_words = list(stopwords.words("english"))  # Convertește în listă

# 1. Preprocesare
# Încărcăm modelul spaCy pentru limba engleză (pentru exemplu)
nlp_processor = spacy.load(
    "en_core_web_sm"
)  # înlocuiește cu "ro_core_news_sm" pentru română, după instalare
doc = nlp_processor(text.lower())

# 2. Lematizare și eliminarea stopwords
filtered_text = " ".join(
    [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
)

# 3. Calculul frecvenței cuvintelor prin TF-IDF
vectorizer = TfidfVectorizer(stop_words=stop_words)  # `stop_words` este acum o listă
X = vectorizer.fit_transform([filtered_text])
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = X.toarray()[0]

# 4. Sortăm cuvintele după relevanță
important_words = sorted(
    zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True
)

# Extragem doar cuvintele într-un vector de stringuri
word_vector = [word for word, score in important_words if score > 0]

print(word_vector)
