"""
transform.py
------------

Step 3 of the ETL pipeline.

Clean the raw AML transaction dataset and create the cleaned dataset
used for downstream feature engineering.

Note:
Duplicate removal is performed within each processing chunk.
"""

import pandas as pd

from src.config import (
    RAW_CSV_FILE,
    CLEANED_CSV_FILE,
    CHUNK_SIZE,
    FRAUD_RELEVANT_TYPES,
)


def clean_dataset():
    """
    Clean the raw AML dataset in chunks and save the processed result.

    Steps:
    - Read the raw dataset in chunks
    - Remove duplicate rows within each chunk
    - Remove rows containing missing values
    - Keep fraud-relevant transaction types
    - Ensure transaction amount is numeric
    - Remove invalid or negative transaction amounts
    - Append cleaned chunks into one CSV
    """

    print("\nCleaning dataset...\n")

    first_chunk = True
    total_rows_written = 0

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            RAW_CSV_FILE,
            chunksize=CHUNK_SIZE,
        ),
        start=1,
    ):

        print(f"Processing chunk {chunk_number}...")

        # Remove duplicate rows within the current chunk
        chunk = chunk.drop_duplicates()

        # Remove rows containing missing values
        chunk = chunk.dropna()

        # Keep only fraud-relevant transaction types
        if FRAUD_RELEVANT_TYPES:
            chunk = chunk[
                chunk["type"].isin(FRAUD_RELEVANT_TYPES)
            ]

        # Ensure amount is numeric
        chunk["amount"] = pd.to_numeric(
            chunk["amount"],
            errors="coerce",
        )

        # Remove rows that became invalid after numeric conversion
        chunk = chunk.dropna(subset=["amount"])

        # Remove invalid negative transaction amounts
        chunk = chunk[
            chunk["amount"] >= 0
        ]

        # Save cleaned chunk
        chunk.to_csv(
            CLEANED_CSV_FILE,
            mode="w" if first_chunk else "a",
            index=False,
            header=first_chunk,
        )

        total_rows_written += len(chunk)
        first_chunk = False

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)
    print(f"Rows written : {total_rows_written:,}")
    print(f"Saved to     : {CLEANED_CSV_FILE}")


if __name__ == "__main__":
    clean_dataset()