"""
validation.py
-------------

Step 2 of the ETL pipeline.

Validate the raw transaction dataset before transformation.
"""

import pandas as pd

from src.config import RAW_CSV_FILE, CHUNK_SIZE


REQUIRED_COLUMNS = {
    "step",
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "newbalanceOrig",
    "nameDest",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
}


def validate_dataset():
    """
    Validate the raw transaction dataset in chunks.

    Checks:
    - required columns are present
    - dataset is not empty
    - isFraud contains only 0/1 values
    - transaction amount is not negative
    - summary fraud metrics are calculated
    """

    print("\nValidation started...\n")

    total_rows = 0
    total_fraud = 0
    total_negative_amounts = 0
    invalid_fraud_values = set()

    columns_checked = False

    for chunk in pd.read_csv(
        RAW_CSV_FILE,
        chunksize=CHUNK_SIZE,
    ):

        if not columns_checked:
            missing_columns = REQUIRED_COLUMNS - set(chunk.columns)

            if missing_columns:
                raise ValueError(
                    "Missing required columns: "
                    f"{sorted(missing_columns)}"
                )

            columns_checked = True

        total_rows += len(chunk)

        total_fraud += int(
            chunk["isFraud"].eq(1).sum()
        )

        invalid_values = set(
            chunk.loc[
                ~chunk["isFraud"].isin([0, 1]),
                "isFraud",
            ]
            .dropna()
            .unique()
        )

        invalid_fraud_values.update(invalid_values)

        total_negative_amounts += int(
            (chunk["amount"] < 0).sum()
        )

    if total_rows == 0:
        raise ValueError("Dataset is empty.")

    if invalid_fraud_values:
        raise ValueError(
            "Invalid values found in isFraud: "
            f"{sorted(invalid_fraud_values)}"
        )

    fraud_percentage = (
        total_fraud / total_rows
    ) * 100

    print("=" * 50)
    print("DATASET VALIDATION SUMMARY")
    print("=" * 50)

    print(f"Total Transactions : {total_rows:,}")
    print(f"Fraud Transactions : {total_fraud:,}")
    print(f"Fraud Percentage   : {fraud_percentage:.4f}%")
    print(f"Negative Amounts   : {total_negative_amounts:,}")

    if total_negative_amounts > 0:
        print("\nWarning: negative transaction amounts detected.")
    else:
        print("\nValidation completed successfully.")


if __name__ == "__main__":
    validate_dataset()