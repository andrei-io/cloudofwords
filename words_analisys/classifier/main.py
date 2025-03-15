import sqlite3
import numpy as np
import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from typing import List, Dict

# Download necessary resources
nltk.download("stopwords")

# Load Spacy model globally for efficiency
nlp = spacy.load("en_core_web_sm")
stop_words = list(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Preprocesses text by converting to lowercase and lemmatizing words.
    It does NOT remove stopwords for TF-IDF purposes.
    """
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha]  # Keep all words
    return " ".join(tokens)


def compute_tf_idf_scores(text: str) -> List[Dict[str, float]]:
    """
    Computes TF-IDF scores for every word in the given text (without using a corpus).

    Parameters:
        text (str): The input sentence to analyze.

    Returns:
        List[Dict[str, float]]: A list of dictionaries containing words and their raw TF-IDF scores.
    """
    # Preprocess the input text
    processed_text = preprocess_text(text)

    # Compute TF-IDF (only for the given text)
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = vectorizer.fit_transform([processed_text])
    feature_names = vectorizer.get_feature_names_out()

    # Extract scores for the text
    text_tfidf = tfidf_matrix.toarray().flatten()

    # Return as a list of dictionaries
    return [
        {"word": word, "score": score} for word, score in zip(feature_names, text_tfidf)
    ]


def normalize_tfidf_scores(
    tfidf_scores: List[Dict[str, float]],
) -> List[Dict[str, float]]:
    """
    Normalizes TF-IDF scores by making their sum equal to 100%.

    Parameters:
        tfidf_scores (List[Dict[str, float]]): Raw TF-IDF scores.

    Returns:
        List[Dict[str, float]]: Normalized TF-IDF scores as percentages.
    """
    total_score = sum(item["score"] for item in tfidf_scores)

    if total_score == 0:
        return [{"word": item["word"], "score": 0} for item in tfidf_scores]

    return [
        {"word": item["word"], "score": (item["score"] / total_score) * 100}
        for item in tfidf_scores
    ]


def get_keywords_from_db():
    # Connect to SQLite database (adjust path if necessary)
    conn = sqlite3.connect("db/filtered_keywords.db")
    cursor = conn.cursor()

    # Fetch all keywords from the table
    cursor.execute("SELECT keyword FROM keywords")
    keywords = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return a list of keywords
    return [keyword[0] for keyword in keywords]


def calculate_scientist_score(text):
    # Fetch the list of keywords from the database
    db_keywords = get_keywords_from_db()

    # Compute the TF-IDF scores for the given text
    tfidf_scores = compute_tf_idf_scores(text)

    for i in tfidf_scores:
        print(i["score"])

    # Normalize the TF-IDF scores for all words
    normalized_scores = normalize_tfidf_scores(tfidf_scores)

    db_words_in_text = [
        item["word"] for item in normalized_scores if item["word"] in db_keywords
    ]

    print(f"Words found in the database: {db_words_in_text}")
    # Sum up the normalized scores for words found in the database
    total_score = sum(
        item["score"] for item in normalized_scores if item["word"] in db_keywords
    )

    return total_score, normalized_scores


def main(sentence):
    # Calculate the normalized TF-IDF score for keywords found in the database
    total_score, normalized_scores = calculate_scientist_score(sentence)

    # Print the normalized scores for all words
    # print("Normalized TF-IDF scores (percentage of total score for each word):")
    # for item in normalized_scores:
    #     print(f"{item['word']}: {item['score']:.2f}%")

    # Print the total score of the words found in the database
    print(f"\nTotal normalized TF-IDF score for database keywords: {total_score:.2f}%")


if __name__ == "__main__":
    # Example usage
    sentence = "Clobotics provides intelligent computer vision solutions for the retail and wind power sectors. The company's end-to-end solutions integrate computer vision, artificial intelligence or machine learning, and data analytics software with different hardware form factors like autonomous drones, mobile applications, and other Internet-of-Things devices for companies to automate time-intensive operational processes, increase efficiencies, and boost the bottom line through the use of real-time, data-driven insights, and analysis. The company's solutions are powered by an international research and development team of rare engineering power. It has filed more than 30 patents to-date. Clobotics was founded by Claire Chen, George Yan, Yan Ke, and Zhao Li in November 2016 and has headquarters in Shanghai, China and Seattle, Washington."
    # sentence = """One of my favorite recipes is a classic vegetable stir-fry. It’s simple but packed with flavor. I start by sautéing a mix of colorful vegetables like bell peppers, carrots, broccoli, and snap peas in a little sesame oil. Then, I add garlic, ginger, and a splash of soy sauce for a savory kick. It’s quick, healthy, and so versatile—you can swap in any veggies you like or add tofu for extra protein. Served over rice, it's an easy, satisfying dish!"""
    #     sentence = """Indulge in the rich and comforting flavors of this creamy garlic parmesan chicken, a dish that perfectly balances savory, creamy, and aromatic elements. Succulent chicken breasts are seared to golden perfection, locking in their natural juices before being bathed in a velvety garlic parmesan sauce. The combination of butter, heavy cream, and freshly grated parmesan creates a luxurious texture, while the addition of minced garlic infuses the dish with an irresistible depth of flavor. A touch of Italian seasoning and a hint of red pepper flakes elevate the taste, making every bite a delightful experience.What makes this recipe truly special is its versatility. While it's elegant enough for a dinner party, it's also simple enough for a cozy weeknight meal. The preparation is straightforward, requiring only a handful of common pantry ingredients. Whether served over a bed of al dente pasta, creamy mashed potatoes, or a side of roasted vegetables, this dish effortlessly complements a variety of accompaniments. The rich sauce clings beautifully to the chicken, ensuring each bite is packed with flavor and warmth.
    # For those looking to customize, this recipe allows for easy modifications to suit different preferences. You can swap chicken breasts for tender thighs for an even juicier result or add sautéed mushrooms and spinach for extra depth and nutrition. A splash of white wine can bring a subtle acidity that balances the richness of the sauce, while a squeeze of fresh lemon juice just before serving enhances the brightness of the dish. Garnishing with fresh parsley or basil adds a final touch of freshness, making the dish even more visually appealing.
    # With its luscious texture, bold flavors, and effortless elegance, this creamy garlic parmesan chicken is bound to become a household favorite. Whether you’re cooking for family, friends, or simply treating yourself to a comforting meal, this dish delivers satisfaction in every bite. Pair it with a crisp white wine or a light salad to round out the meal, and enjoy the comforting embrace of this timeless, restaurant-quality recipe from the comfort of your home."""

    main(sentence)
