import nltk
from rake_nltk import Rake

# Descarcă resursele necesare pentru NLTK
nltk.download("punkt")


def extract_rake_keywords(text, max_length=1) -> list[str]:
    """
    Extrage cuvinte cheie dintr-un text folosind RAKE (Rapid Automatic Keyword Extraction).

    Parameters:
        text (str): Textul din care vor fi extrase cuvintele cheie.
        max_length (int): Lungimea maximă a unei fraze cheie (în număr de cuvinte). Implicit este 1.

    Returns:
        list[str]: O listă de stringuri reprezentând cuvintele cheie extrase, ordonate după scorul de importanță.
    """
    # Verifică dacă textul este gol
    if not text:
        raise ValueError(
            "Textul preprocesat este gol. Verificați conținutul textului de intrare."
        )
    # Inițializează RAKE cu lungimea maximă specificată pentru fraze
    r = Rake(max_length=max_length)

    # Extrage cuvintele cheie din text
    r.extract_keywords_from_text(text)

    # Obține frazele cheie ordonate după scor și returnează ca o listă de stringuri
    keywords = r.get_ranked_phrases()

    return keywords
