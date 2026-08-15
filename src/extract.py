"""
extract.py
-----------
Step 1 of the ETL Pipeline
Read the raw AML transaction dataset.
"""

from pathlib import Path
import pandas as pd

# Project Root Folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw Data Folder
RAW_DATA_FOLDER = PROJECT_ROOT / "data" / "raw"

# CSV File
CSV_FILE = RAW_DATA_FOLDER / "PS_20174392719_1491204439457_log.csv"


def load_sample(rows=5):
    """
    Load only the first few rows of the dataset.
    """
    df = pd.read_csv(CSV_FILE, nrows=rows)
    return df


def count_rows():
    """
    Count the total number of transaction rows
    without loading the complete dataset into memory.
    """
    row_count = 0

    for chunk in pd.read_csv(
        CSV_FILE,
        usecols=["step"],
        chunksize=500_000
    ):
        row_count += len(chunk)

    return row_count


if __name__ == "__main__":

    print("=" * 60)
    print(" AML Fraud Analytics Project ")
    print("=" * 60)

    # Load first 5 rows
    df = load_sample()

    print("\nFirst 5 Rows\n")
    print(df)

    print("\nColumn Names\n")
    print(df.columns.tolist())

    print("\nCounting total transactions...")

    total_rows = count_rows()

    print(f"Total Transactions: {total_rows:,}")