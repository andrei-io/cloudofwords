import json
import numpy as np
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(vector1, vector2):
    """Calculate cosine similarity between two vectors using scikit-learn."""
    return cosine_similarity([vector1], [vector2])[0][0]


def load_average_vectors(json_file):
    """Load average vectors from a JSON file and convert them to NumPy arrays."""
    with open(json_file, "r") as f:
        data = json.load(f)
    return {origin: np.array(vector) for origin, vector in data.items()}


def compute_pairwise_cosine_similarities(vectors_dict):
    """
    Compute a full cosine similarity matrix for all origins.

    Returns a dictionary where each key is an origin and the value is another
    dictionary mapping every other origin (including itself) to its cosine similarity.
    """
    origins = list(vectors_dict.keys())
    # Initialize the similarity matrix with self-similarity of 1.0
    similarities_matrix = {origin: {} for origin in origins}
    for origin in origins:
        similarities_matrix[origin][origin] = 1.0

    # Calculate similarity for each unique pair and store in both directions
    for origin1, origin2 in combinations(origins, 2):
        sim = calculate_cosine_similarity(vectors_dict[origin1], vectors_dict[origin2])
        similarities_matrix[origin1][origin2] = sim
        similarities_matrix[origin2][origin1] = sim

    return similarities_matrix


def display_similarities(similarities_matrix):
    """Display the full similarity matrix in a tabular format with padded columns."""
    origins = list(similarities_matrix.keys())
    # Determine the maximum width for the origin names
    max_width = max(len(origin) for origin in origins) + 2  # adding extra padding

    # Create header row with padded origin names
    header = " ".ljust(max_width) + "".join(
        f"{origin:<{max_width}}" for origin in origins
    )
    print(header)

    # Print each row with padded values
    for origin in origins:
        row = f"{origin:<{max_width}}"
        for other in origins:
            sim = similarities_matrix[origin].get(other, 0.0)
            row += f"{sim: <{max_width}.4f}"
        print(row)


def main():
    # Path to the JSON file with average vectors computed using the Google News Word2Vec model
    input_file = "average_vectors_by_origin2.json"
    vectors_dict = load_average_vectors(input_file)

    # Compute pairwise cosine similarities
    similarities_matrix = compute_pairwise_cosine_similarities(vectors_dict)

    # Display the similarities in a padded table
    print("Pairwise Cosine Similarities:")
    display_similarities(similarities_matrix)

    # Optionally, save the similarities to a JSON file
    output_file = "pairwise_cosine_similarities.json"
    with open(output_file, "w") as f:
        json.dump(similarities_matrix, f, indent=4)
    print(f"\nPairwise cosine similarities saved to {output_file}")


if __name__ == "__main__":
    main()
