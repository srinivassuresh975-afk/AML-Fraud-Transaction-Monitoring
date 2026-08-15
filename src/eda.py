"""
eda.py
------

Step 5 of the AML Fraud Analytics ETL pipeline.

Perform exploratory analysis on the enriched transaction dataset
and create summary CSV files for reporting and Power BI.
"""

import pandas as pd

from src.config import (
    ENRICHED_CSV_FILE,
    REPORTS_FOLDER,
    CHUNK_SIZE,
)


REQUIRED_COLUMNS = {
    "amount",
    "isFraud",
    "type",
    "risk_level",
    "is_large_transaction",
    "is_very_large_transaction",
    "structuring_proxy_flag",
    "origin_account_emptied",
    "destination_was_empty",
    "origin_balance_mismatch",
    "destination_balance_mismatch",
    "high_risk_transaction_type",
}


RED_FLAG_COLUMNS = [
    "is_large_transaction",
    "is_very_large_transaction",
    "structuring_proxy_flag",
    "origin_account_emptied",
    "destination_was_empty",
    "origin_balance_mismatch",
    "destination_balance_mismatch",
    "high_risk_transaction_type",
]


def run_eda():
    """
    Analyze the enriched AML transaction dataset and generate
    summary reporting files.
    """

    print("\n" + "=" * 60)
    print("AML FRAUD ANALYTICS - EDA & REPORTING")
    print("=" * 60)

    if not ENRICHED_CSV_FILE.exists():
        raise FileNotFoundError(
            f"Enriched dataset not found: {ENRICHED_CSV_FILE}"
        )

    REPORTS_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"\nInput file : {ENRICHED_CSV_FILE}")
    print(f"Chunk size : {CHUNK_SIZE:,}")

    total_transactions = 0
    total_amount = 0.0
    total_fraud_transactions = 0
    total_fraud_amount = 0.0

    transaction_type_summary = {}
    risk_level_summary = {}

    red_flag_summary = {
        column: 0
        for column in RED_FLAG_COLUMNS
    }

    schema_checked = False

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            ENRICHED_CSV_FILE,
            chunksize=CHUNK_SIZE,
        ),
        start=1,
    ):

        print(f"Processing EDA chunk {chunk_number}...")

        if not schema_checked:
            missing_columns = (
                REQUIRED_COLUMNS
                - set(chunk.columns)
            )

            if missing_columns:
                raise ValueError(
                    "Missing required EDA columns: "
                    f"{sorted(missing_columns)}"
                )

            schema_checked = True

        total_transactions += len(chunk)

        total_amount += float(
            chunk["amount"].sum()
        )

        fraud_mask = (
            chunk["isFraud"] == 1
        )

        total_fraud_transactions += int(
            fraud_mask.sum()
        )

        total_fraud_amount += float(
            chunk.loc[
                fraud_mask,
                "amount",
            ].sum()
        )

        type_counts = (
            chunk["type"]
            .value_counts()
        )

        for transaction_type, count in type_counts.items():
            transaction_type_summary[
                transaction_type
            ] = (
                transaction_type_summary.get(
                    transaction_type,
                    0,
                )
                + int(count)
            )

        risk_counts = (
            chunk["risk_level"]
            .value_counts()
        )

        for risk_level, count in risk_counts.items():
            risk_level_summary[
                risk_level
            ] = (
                risk_level_summary.get(
                    risk_level,
                    0,
                )
                + int(count)
            )

        for column in RED_FLAG_COLUMNS:
            red_flag_summary[
                column
            ] += int(
                chunk[column].sum()
            )

    if total_transactions == 0:
        raise ValueError(
            "Enriched dataset is empty."
        )

    fraud_percentage = (
        total_fraud_transactions
        / total_transactions
    ) * 100

    average_transaction_amount = (
        total_amount
        / total_transactions
    )

    aml_summary_df = pd.DataFrame(
        {
            "Metric": [
                "Total Transactions",
                "Total Transaction Amount",
                "Average Transaction Amount",
                "Fraud Transactions",
                "Fraud Percentage",
                "Fraud Amount",
            ],
            "Value": [
                total_transactions,
                total_amount,
                average_transaction_amount,
                total_fraud_transactions,
                fraud_percentage,
                total_fraud_amount,
            ],
        }
    )

    transaction_type_df = pd.DataFrame(
        list(
            transaction_type_summary.items()
        ),
        columns=[
            "Transaction Type",
            "Transaction Count",
        ],
    )

    if not transaction_type_df.empty:
        transaction_type_df = (
            transaction_type_df
            .sort_values(
                by="Transaction Count",
                ascending=False,
            )
        )

    risk_level_df = pd.DataFrame(
        list(
            risk_level_summary.items()
        ),
        columns=[
            "Risk Level",
            "Transaction Count",
        ],
    )

    if not risk_level_df.empty:
        risk_level_df = (
            risk_level_df
            .sort_values(
                by="Transaction Count",
                ascending=False,
            )
        )

    red_flag_df = pd.DataFrame(
        list(
            red_flag_summary.items()
        ),
        columns=[
            "Red Flag",
            "Transaction Count",
        ],
    )

    if not red_flag_df.empty:
        red_flag_df = (
            red_flag_df
            .sort_values(
                by="Transaction Count",
                ascending=False,
            )
        )

    aml_summary_file = (
        REPORTS_FOLDER
        / "aml_summary.csv"
    )

    transaction_type_file = (
        REPORTS_FOLDER
        / "transaction_type_summary.csv"
    )

    risk_level_file = (
        REPORTS_FOLDER
        / "risk_level_summary.csv"
    )

    red_flag_file = (
        REPORTS_FOLDER
        / "red_flag_summary.csv"
    )

    aml_summary_df.to_csv(
        aml_summary_file,
        index=False,
    )

    transaction_type_df.to_csv(
        transaction_type_file,
        index=False,
    )

    risk_level_df.to_csv(
        risk_level_file,
        index=False,
    )

    red_flag_df.to_csv(
        red_flag_file,
        index=False,
    )

    print("\n" + "=" * 60)
    print("EDA SUMMARY")
    print("=" * 60)

    print(
        f"Total Transactions       : "
        f"{total_transactions:,}"
    )

    print(
        f"Total Transaction Amount : "
        f"{total_amount:,.2f}"
    )

    print(
        f"Average Transaction      : "
        f"{average_transaction_amount:,.2f}"
    )

    print(
        f"Fraud Transactions       : "
        f"{total_fraud_transactions:,}"
    )

    print(
        f"Fraud Percentage         : "
        f"{fraud_percentage:.4f}%"
    )

    print(
        f"Fraud Amount             : "
        f"{total_fraud_amount:,.2f}"
    )

    print("\nTransaction Type Summary:")
    print(
        transaction_type_df.to_string(
            index=False
        )
    )

    print("\nRisk Level Summary:")
    print(
        risk_level_df.to_string(
            index=False
        )
    )

    print("\nRed Flag Summary:")
    print(
        red_flag_df.to_string(
            index=False
        )
    )

    print("\n" + "=" * 60)
    print("EDA & REPORTING COMPLETED")
    print("=" * 60)

    print("\nReports saved to:")
    print(REPORTS_FOLDER)

    print("\nGenerated files:")
    print("1. aml_summary.csv")
    print("2. transaction_type_summary.csv")
    print("3. risk_level_summary.csv")
    print("4. red_flag_summary.csv")


if __name__ == "__main__":
    run_eda()