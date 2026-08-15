"""
validation.py
----------------
Step 2 of the ETL Pipeline

Purpose:
Validate the raw AML transaction dataset.
"""

from pathlib import Path
import pandas as pd

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw Data Folder
RAW_DATA_FOLDER = PROJECT_ROOT / "data" / "raw"

# CSV File
CSV_FILE = RAW_DATA_FOLDER / "PS_20174392719_1491204439457_log.csv"

# Read 500,000 rows at a time
CHUNK_SIZE = 500_000


def validate_dataset():

    print("Validation Started...\n")

    total_rows = 0
    total_fraud = 0

    for chunk in pd.read_csv(
        CSV_FILE,
        chunksize=CHUNK_SIZE
    ):

        total_rows += len(chunk)
        total_fraud += chunk["isFraud"].sum()

    print("=" * 50)
    print("DATASET SUMMARY")
    print("=" * 50)

    print(f"Total Transactions : {total_rows:,}")
    print(f"Fraud Transactions : {total_fraud:,}")

    fraud_percentage = (total_fraud / total_rows) * 100

    print(f"Fraud Percentage : {fraud_percentage:.4f}%")

 
if __name__ == "__main__":
    validate_dataset()
    