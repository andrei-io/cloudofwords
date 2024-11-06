import pandas as pd
import concurrent.futures
from tqdm import tqdm  # Pentru afișarea progresului
from lda_model import extract_lda_keywords
from rake_model import extract_rake_keywords
from text_rank_model import extract_textrank_keywords
from tf_idf_model import extract_tfidf_keywords
from nltk.corpus import stopwords
import nltk

# Încărcăm resursele NLTK înainte de multi-threading
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Citește un fișier Excel
df = pd.read_excel("./abstracts.xlsx")


# Funcția care procesează un singur rând
def process_row(row):
    index, title, abstract = row["Index"], row["Title"], row["Abstract"]

    # Extrage cuvinte cheie folosind LDA
    lda_keywords = ", ".join(extract_lda_keywords(abstract))

    # Extrage cuvinte cheie folosind RAKE
    rake_keywords = ", ".join(extract_rake_keywords(abstract))

    # Extrage cuvinte cheie folosind TextRank
    textrank_keywords = ", ".join(extract_textrank_keywords(abstract))

    # Extrage cuvinte cheie folosind TF-IDF
    tfidf_keywords = ", ".join(extract_tfidf_keywords(abstract))

    # Returnează un dicționar cu rezultatele
    return {
        "Index": index,
        "LDA_Keywords": lda_keywords,
        "RAKE_Keywords": rake_keywords,
        "TextRank_Keywords": textrank_keywords,
        "TF-IDF_Keywords": tfidf_keywords,
    }


# Adaugă o coloană de index pentru a păstra ordinea inițială
df = df.reset_index().rename(columns={"index": "Index"})

# Folosește un ThreadPoolExecutor pentru a procesa rândurile în paralel
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Aplică funcția pe fiecare rând și urmărește progresul cu tqdm
    results = list(
        tqdm(
            executor.map(process_row, [row for _, row in df.iterrows()]),
            total=len(df),
            desc="Processing abstracts",
        )
    )

# Convertim rezultatele într-un DataFrame
result_df = pd.DataFrame(results).set_index("Index").sort_index()

# Adaugă coloanele cu cuvintele cheie la DataFrame-ul original
df["LDA_Keywords"] = result_df["LDA_Keywords"]
df["RAKE_Keywords"] = result_df["RAKE_Keywords"]
df["TextRank_Keywords"] = result_df["TextRank_Keywords"]
df["TF-IDF_Keywords"] = result_df["TF-IDF_Keywords"]

# Salvează rezultatul într-un nou fișier Excel
df.to_excel("./abstracts_with_keywords.xlsx", index=False)
print("Extractie cuvinte cheie finalizata!")
