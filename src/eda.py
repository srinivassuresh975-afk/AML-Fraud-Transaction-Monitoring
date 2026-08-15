"""
eda.py
------------------------------------------------------------
Step 5 of the AML Fraud Analytics ETL Pipeline

Purpose:
Perform Exploratory Data Analysis on the enriched AML dataset
and create summary CSV files for Power BI and reporting.
------------------------------------------------------------
"""

import pandas as pd

from src.config import (
    ENRICHED_CSV_FILE,
    REPORTS_FOLDER,
    CHUNK_SIZE,
)


def run_eda():
    """
    Analyze the enriched AML transaction dataset and generate
    summary reporting files.
    """

    print("\n" + "=" * 60)
    print("AML FRAUD ANALYTICS - EDA & REPORTING")
    print("=" * 60)

    # ---------------------------------------------------------
    # VALIDATE INPUT FILE
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # GLOBAL METRICS
    # ---------------------------------------------------------

    total_transactions = 0
    total_amount = 0.0

    total_fraud_transactions = 0
    total_fraud_amount = 0.0


    # ---------------------------------------------------------
    # SUMMARY CONTAINERS
    # ---------------------------------------------------------

    transaction_type_summary = {}

    risk_level_summary = {}


    # ---------------------------------------------------------
    # RED FLAG COLUMNS
    # ---------------------------------------------------------

    red_flag_columns = [
        "is_large_transaction",
        "is_very_large_transaction",
        "structuring_flag",
        "origin_account_emptied",
        "destination_was_empty",
        "origin_balance_mismatch",
        "destination_balance_mismatch",
        "high_risk_transaction_type",
    ]

    red_flag_summary = {
        column: 0
        for column in red_flag_columns
    }


    # ---------------------------------------------------------
    # PROCESS ENRICHED DATASET IN CHUNKS
    # ---------------------------------------------------------

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            ENRICHED_CSV_FILE,
            chunksize=CHUNK_SIZE,
        ),
        start=1,
    ):

        print(
            f"Processing EDA chunk "
            f"{chunk_number}..."
        )


        # =====================================================
        # TOTAL TRANSACTIONS
        # =====================================================

        total_transactions += len(chunk)


        # =====================================================
        # TOTAL AMOUNT
        # =====================================================

        if "amount" in chunk.columns:

            total_amount += float(
                chunk["amount"].sum()
            )


        # =====================================================
        # FRAUD METRICS
        # =====================================================

        if "isFraud" in chunk.columns:

            fraud_mask = (
                chunk["isFraud"] == 1
            )

            total_fraud_transactions += int(
                fraud_mask.sum()
            )

            if "amount" in chunk.columns:

                total_fraud_amount += float(
                    chunk.loc[
                        fraud_mask,
                        "amount",
                    ].sum()
                )


        # =====================================================
        # TRANSACTION TYPE SUMMARY
        # =====================================================

        if "type" in chunk.columns:

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


        # =====================================================
        # RISK LEVEL SUMMARY
        # =====================================================

        if "risk_level" in chunk.columns:

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


        # =====================================================
        # RED FLAG SUMMARY
        # =====================================================

        for column in red_flag_columns:

            if column in chunk.columns:

                red_flag_summary[
                    column
                ] += int(
                    chunk[column].sum()
                )


    # ---------------------------------------------------------
    # CALCULATED METRICS
    # ---------------------------------------------------------

    if total_transactions > 0:

        fraud_percentage = (
            total_fraud_transactions
            / total_transactions
        ) * 100

        average_transaction_amount = (
            total_amount
            / total_transactions
        )

    else:

        fraud_percentage = 0.0

        average_transaction_amount = 0.0


    # =========================================================
    # AML SUMMARY
    # =========================================================

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


    # =========================================================
    # TRANSACTION TYPE SUMMARY
    # =========================================================

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


    # =========================================================
    # RISK LEVEL SUMMARY
    # =========================================================

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


    # =========================================================
    # RED FLAG SUMMARY
    # =========================================================

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


    # =========================================================
    # SAVE REPORTS
    # =========================================================

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


    # =========================================================
    # DISPLAY SUMMARY
    # =========================================================

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


    # =========================================================
    # DISPLAY TRANSACTION TYPE SUMMARY
    # =========================================================

    print("\nTransaction Type Summary:")

    if transaction_type_df.empty:

        print("No transaction type data.")

    else:

        print(
            transaction_type_df.to_string(
                index=False
            )
        )


    # =========================================================
    # DISPLAY RISK LEVEL SUMMARY
    # =========================================================

    print("\nRisk Level Summary:")

    if risk_level_df.empty:

        print("No risk level data.")

    else:

        print(
            risk_level_df.to_string(
                index=False
            )
        )


    # =========================================================
    # DISPLAY RED FLAG SUMMARY
    # =========================================================

    print("\nRed Flag Summary:")

    if red_flag_df.empty:

        print("No red flag data.")

    else:

        print(
            red_flag_df.to_string(
                index=False
            )
        )


    # =========================================================
    # COMPLETION
    # =========================================================

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