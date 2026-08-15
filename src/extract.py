"""
extract.py
----------

Step 1 of the ETL pipeline.

Provides lightweight inspection of the raw transaction dataset
without loading the complete file into memory.
"""

import pandas as pd

from src.config import RAW_CSV_FILE, CHUNK_SIZE


def load_sample(rows=5):
    """Return the first few rows of the raw transaction dataset."""

    return pd.read_csv(
        RAW_CSV_FILE,
        nrows=rows,
    )


def count_rows():
    """Count transaction rows using chunked processing."""

    row_count = 0

    for chunk in pd.read_csv(
        RAW_CSV_FILE,
        usecols=["step"],
        chunksize=CHUNK_SIZE,
    ):
        row_count += len(chunk)

    return row_count


if __name__ == "__main__":

    print("=" * 60)
    print("AML Fraud Analytics - Raw Data Inspection")
    print("=" * 60)

    df = load_sample()

    print("\nFirst 5 rows:\n")
    print(df)

    print("\nColumn names:\n")
    print(df.columns.tolist())

    print("\nCounting total transactions...")

    total_rows = count_rows()

    print(f"\nTotal transactions: {total_rows:,}")