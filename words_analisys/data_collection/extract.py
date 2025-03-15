import os
import pandas as pd
from lda_model import extract_lda_keywords
from rake_model import extract_rake_keywords
from text_rank_model import extract_textrank_keywords
from tf_idf_model import extract_tfidf_keywords
import argparse


def extract_keywords_to_excel(input_filename: str, column_name: str = "abstract"):
    """
    Procesează un fișier Excel pentru a extrage cuvinte cheie și salvează rezultatele într-un fișier nou.

    Parameters:
        input_filename (str): Calea către fișierul Excel de intrare.
    """
    # Verifică dacă fișierul există
    if not os.path.exists(input_filename):
        print(f"Eroare: Fișierul {input_filename} nu a fost găsit.")
        return

    # Citește fișierul Excel
    df = pd.read_excel(input_filename)

    # Inițializăm liste pentru a adăuga cuvintele cheie extrase în DataFrame
    lda_keywords_list = []
    rake_keywords_list = []
    textrank_keywords_list = []
    tfidf_keywords_list = []

    # Iterează prin fiecare rând din DataFrame
    for index, row in df.iterrows():
        print(f"Processing Abstract {index + 1} of {df.shape[0]}")

        abstract = row[column_name]

        # Extrage cuvinte cheie folosind fiecare metodă
        try:
            lda_keywords_list.append(", ".join(extract_lda_keywords(abstract)))
        except Exception as e:
            print(f"Error extracting LDA keywords for Abstract {index + 1}: {e}")
            lda_keywords_list.append("")

        try:
            rake_keywords_list.append(", ".join(extract_rake_keywords(abstract)))
        except Exception as e:
            print(f"Error extracting RAKE keywords for Abstract {index + 1}: {e}")
            rake_keywords_list.append("")

        try:
            textrank_keywords_list.append(
                ", ".join(extract_textrank_keywords(abstract))
            )
        except Exception as e:
            print(f"Error extracting TextRank keywords for Abstract {index + 1}: {e}")
            textrank_keywords_list.append("")

        try:
            tfidf_keywords_list.append(", ".join(extract_tfidf_keywords(abstract)))
        except Exception as e:
            print(f"Error extracting TF-IDF keywords for Abstract {index + 1}: {e}")
            tfidf_keywords_list.append("")

    # Adăugăm coloanele cu cuvintele cheie în DataFrame
    df["LDA_Keywords"] = lda_keywords_list
    df["RAKE_Keywords"] = rake_keywords_list
    df["TextRank_Keywords"] = textrank_keywords_list
    df["TF-IDF_Keywords"] = tfidf_keywords_list

    # Creăm directorul de ieșire dacă nu există, subforma output/base_filename/output_chunk1.xlsx
    os.makedirs("output", exist_ok=True)

    # Definim calea fișierului de ieșire
    output_filename = os.path.join("output", os.path.basename(input_filename))

    # Salvează rezultatul într-un nou fișier Excel
    df.to_excel(output_filename, index=False)
    print(
        f"Extractie cuvinte cheie finalizata! Rezultatele sunt salvate in {output_filename}"
    )


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract keywords and save to output file."
    )
    parser.add_argument("filename", type=str, help="The name of the input Excel file.")
    parser.add_argument(
        "--column_name",
        type=str,
        default="abstract",
        help="The name of the column containing the text data.",
    )
    args = parser.parse_args()

    # Call the function with the provided filename
    extract_keywords_to_excel(args.filename, args.column_name)
