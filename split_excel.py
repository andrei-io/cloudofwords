import pandas as pd
import os


def split_excel_file(
    filename: str, output_dir: str = "output_chunks", chunk_size: int = 3000
):
    """
    Splits a large Excel file into smaller Excel files (chunks).

    Parameters:
        filename (str): The path to the large Excel file to split.
        output_dir (str): The directory where the chunk files will be saved.
        chunk_size (int): Number of rows per chunk file.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the entire Excel file
    try:
        df = pd.read_excel(filename)
        total_rows = df.shape[0]

        # Split into chunks
        for i in range(0, total_rows, chunk_size):
            chunk = df[i : i + chunk_size]
            chunk_filename = os.path.join(
                output_dir,
                f"{os.path.splitext(os.path.basename(filename))[0]}_chunk_{i//chunk_size + 1}.xlsx",
            )
            chunk.to_excel(chunk_filename, index=False)
            print(f"Chunk {i // chunk_size + 1} saved as {chunk_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    import argparse

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Split a large Excel file into smaller chunks."
    )
    parser.add_argument("filename", type=str, help="The path to the input Excel file.")
    parser.add_argument(
        "--output_dir",
        type=str,
        default="output_chunks",
        help="Directory to save the output chunks.",
    )
    parser.add_argument(
        "--chunk_size", type=int, default=3000, help="Number of rows per chunk file."
    )
    args = parser.parse_args()

    # Run the function with provided arguments
    split_excel_file(args.filename, args.output_dir, args.chunk_size)
