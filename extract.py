import pandas as pd
from lda_model import extract_lda_keywords
from rake_model import extract_rake_keywords
from text_rank_model import extract_textrank_keywords
from tf_idf_model import extract_tfidf_keywords

# Citește un fișier Excel
df = pd.read_excel("./abstracts.xlsx")

# Inițializăm liste pentru a adăuga cuvintele cheie extrase în DataFrame
lda_keywords_list = []
rake_keywords_list = []
textrank_keywords_list = []
tfidf_keywords_list = []

# Iterează prin fiecare rând din DataFrame

for index, row in df.iterrows():
    print(f"Processing Abstract {index + 1} of {df.shape[0]}")

    title = row["Title"]
    abstract = row["Abstract"]

    # Extrage cuvinte cheie folosind LDA
    lda_keywords = extract_lda_keywords(abstract)
    lda_keywords_list.append(
        ", ".join(lda_keywords)
    )  # Adăugăm cuvintele cheie ca string

    # Extrage cuvinte cheie folosind RAKE
    rake_keywords = extract_rake_keywords(abstract)
    rake_keywords_list.append(
        ", ".join(rake_keywords)
    )  # Adăugăm cuvintele cheie ca string

    # Extrage cuvinte cheie folosind TextRank
    textrank_keywords = extract_textrank_keywords(abstract)
    textrank_keywords_list.append(
        ", ".join(textrank_keywords)
    )  # Adăugăm cuvintele cheie ca string

    # Extrage cuvinte cheie folosind TF-IDF
    tfidf_keywords = extract_tfidf_keywords(abstract)
    tfidf_keywords_list.append(
        ", ".join(tfidf_keywords)
    )  # Adăugăm cuvintele cheie ca string


# Adăugăm coloanele cu cuvintele cheie în DataFrame
df["LDA_Keywords"] = lda_keywords_list
df["RAKE_Keywords"] = rake_keywords_list
df["TextRank_Keywords"] = textrank_keywords_list
df["TF-IDF_Keywords"] = tfidf_keywords_list

# Salvează rezultatul într-un nou fișier Excel
df.to_excel("./abstracts_with_keywords.xlsx", index=False)
print("Extractie cuvinte cheie finalizata!")
