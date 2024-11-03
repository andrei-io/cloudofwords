import nltk
from rake_nltk import Rake
from nltk.corpus import stopwords

nltk.download("punkt")  # imi trebuie pentru model
nltk.download("punkt_tab")  # imi trebuie pentru model

nltk.download("stopwords")

r = Rake(max_length=1)  # default english, lungimea unei fraze = 1

text = """
The digitalization of data has resulted in a data tsunami in practically every industry of data-driven enterprise. Furthermore, man-to-machine (M2M) digital data handling has dramatically amplified the information wave. There has been a significant development in digital agriculture management applications, which has impacted information and communication technology (ICT) to deliver benefits for both farmers and consumers, as well as pushed technological solutions into rural settings. This paper highlights the potential of ICT technologies in traditional agriculture, as well as the challenges that may arise when they are used in farming techniques. Robotics, Internet of things (IoT) devices, and machine learning issues, as well as the functions of machine learning, artificial intelligence, and sensors in agriculture, are all detailed. In addition, drones are being considered for crop observation as well as crop yield optimization management. When applicable, worldwide and cutting-edge IoT-based farming systems and platforms are also highlighted. We do a thorough review of the most recent literature in each area of expertise. We conclude the present and future trends in artificial intelligence (AI) and highlight existing and emerging research problems in AI in agriculture due to this comprehensive assessment.
"""

stop_words = list(stopwords.words("english"))  # Convertește în listă

r.extract_keywords_from_text(text)

keywords = r.get_ranked_phrases()  # Returnează frazele cheie ordonate după scor

# Afișează cuvintele cheie
print(keywords)
