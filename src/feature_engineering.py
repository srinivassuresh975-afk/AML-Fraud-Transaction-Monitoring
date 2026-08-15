"""
feature_engineering.py
----------------------

Step 4 of the AML Fraud Analytics ETL Pipeline.

Purpose:
Create AML/fraud-related analytical features from the cleaned
transaction dataset and save the enriched dataset for EDA
and Power BI reporting.
"""

import pandas as pd

from src.config import (
    CLEANED_CSV_FILE,
    ENRICHED_CSV_FILE,
    CHUNK_SIZE,
    LARGE_TRANSACTION_THRESHOLD,
    VERY_LARGE_TRANSACTION_THRESHOLD,
    STRUCTURING_LOWER_LIMIT,
    STRUCTURING_UPPER_LIMIT,
)


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def add_features(chunk):
    """
    Add AML and fraud-related features to a dataframe chunk.
    """

    # --------------------------------------------------------
    # 1. FRAUD STATUS
    # --------------------------------------------------------

    chunk["fraud_status"] = chunk["isFraud"].map(
        {
            0: "Legitimate",
            1: "Fraud",
        }
    ).fillna("Unknown")


    # --------------------------------------------------------
    # 2. LARGE TRANSACTION FLAG
    # --------------------------------------------------------

    chunk["is_large_transaction"] = (
        chunk["amount"] >= LARGE_TRANSACTION_THRESHOLD
    ).astype("int8")


    # --------------------------------------------------------
    # 3. VERY LARGE TRANSACTION FLAG
    # --------------------------------------------------------

    chunk["is_very_large_transaction"] = (
        chunk["amount"] >= VERY_LARGE_TRANSACTION_THRESHOLD
    ).astype("int8")


    # --------------------------------------------------------
    # 4. STRUCTURING / SMURFING PROXY
    # --------------------------------------------------------
    # Transactions just below a reporting-style threshold can
    # be useful as an analytical red flag.
    #
    # Important:
    # This is only a proxy indicator, not proof of structuring.
    # --------------------------------------------------------

    chunk["structuring_flag"] = (
        chunk["amount"].between(
            STRUCTURING_LOWER_LIMIT,
            STRUCTURING_UPPER_LIMIT,
            inclusive="left",
        )
    ).astype("int8")


    # --------------------------------------------------------
    # 5. ORIGIN ACCOUNT EMPTIED
    # --------------------------------------------------------
    # Flag when sender had money before the transaction and
    # the resulting balance becomes zero.
    # --------------------------------------------------------

    chunk["origin_account_emptied"] = (
        (chunk["oldbalanceOrg"] > 0)
        & (chunk["newbalanceOrig"] == 0)
        & (chunk["amount"] > 0)
    ).astype("int8")


    # --------------------------------------------------------
    # 6. DESTINATION WAS EMPTY
    # --------------------------------------------------------
    # Receiving account had zero balance before transaction.
    # --------------------------------------------------------

    chunk["destination_was_empty"] = (
        (chunk["oldbalanceDest"] == 0)
        & (chunk["amount"] > 0)
    ).astype("int8")


    # --------------------------------------------------------
    # 7. ORIGIN BALANCE MISMATCH
    # --------------------------------------------------------
    # Expected:
    # old sender balance - amount = new sender balance
    # --------------------------------------------------------

    expected_origin_balance = (
        chunk["oldbalanceOrg"] - chunk["amount"]
    ).clip(lower=0)

    chunk["origin_balance_mismatch"] = (
        (
            expected_origin_balance
            - chunk["newbalanceOrig"]
        ).abs()
        > 1
    ).astype("int8")


    # --------------------------------------------------------
    # 8. DESTINATION BALANCE MISMATCH
    # --------------------------------------------------------
    # Expected:
    # old receiver balance + amount = new receiver balance
    # --------------------------------------------------------

    expected_destination_balance = (
        chunk["oldbalanceDest"] + chunk["amount"]
    )

    chunk["destination_balance_mismatch"] = (
        (
            expected_destination_balance
            - chunk["newbalanceDest"]
        ).abs()
        > 1
    ).astype("int8")


    # --------------------------------------------------------
    # 9. TRANSACTION TYPE RISK FLAG
    # --------------------------------------------------------
    # TRANSFER and CASH_OUT are especially relevant in this
    # fraud dataset.
    # --------------------------------------------------------

    chunk["high_risk_transaction_type"] = (
        chunk["type"].isin(
            [
                "TRANSFER",
                "CASH_OUT",
            ]
        )
    ).astype("int8")


    # --------------------------------------------------------
    # 10. HOUR OF DAY
    # --------------------------------------------------------
    # PaySim step represents an hourly simulation step.
    # Convert it to hour 0-23.
    # --------------------------------------------------------

    chunk["hour_of_day"] = (
        (chunk["step"] - 1) % 24
    ).astype("int8")


    # --------------------------------------------------------
    # 11. DAY NUMBER
    # --------------------------------------------------------

    chunk["day_number"] = (
        ((chunk["step"] - 1) // 24) + 1
    ).astype("int16")


    # --------------------------------------------------------
    # 12. AML RISK SCORE
    # --------------------------------------------------------
    # Weighted analytical score.
    #
    # Maximum score = 100
    # --------------------------------------------------------

    chunk["risk_score"] = (
        chunk["origin_account_emptied"] * 30
        + chunk["destination_was_empty"] * 20
        + chunk["is_large_transaction"] * 15
        + chunk["is_very_large_transaction"] * 10
        + chunk["origin_balance_mismatch"] * 15
        + chunk["destination_balance_mismatch"] * 10
    ).clip(
        upper=100
    ).astype("int16")


    # --------------------------------------------------------
    # 13. RISK LEVEL
    # --------------------------------------------------------

    chunk["risk_level"] = pd.cut(
        chunk["risk_score"],
        bins=[
            -1,
            19,
            49,
            100,
        ],
        labels=[
            "Low",
            "Medium",
            "High",
        ],
    )


    return chunk


# ============================================================
# CREATE ENRICHED DATASET
# ============================================================

def create_enriched_dataset():
    """
    Read the cleaned AML dataset in chunks,
    apply feature engineering,
    and save the enriched dataset.
    """

    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING STARTED")
    print("=" * 60)

    print(f"Input file : {CLEANED_CSV_FILE}")
    print(f"Output file: {ENRICHED_CSV_FILE}")
    print(f"Chunk size : {CHUNK_SIZE:,}")

    # Make sure output directory exists
    ENRICHED_CSV_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Remove old enriched file before rebuilding
    if ENRICHED_CSV_FILE.exists():
        print("\nRemoving previous enriched dataset...")
        ENRICHED_CSV_FILE.unlink()

    total_rows = 0
    first_chunk = True


    # --------------------------------------------------------
    # PROCESS CLEANED DATASET IN CHUNKS
    # --------------------------------------------------------

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            CLEANED_CSV_FILE,
            chunksize=CHUNK_SIZE,
        ),
        start=1,
    ):

        print(
            f"Processing chunk {chunk_number} "
            f"({len(chunk):,} rows)..."
        )

        # Add AML/fraud features
        chunk = add_features(chunk)


        # ----------------------------------------------------
        # SAVE CHUNK
        # ----------------------------------------------------

        chunk.to_csv(
            ENRICHED_CSV_FILE,
            mode="w" if first_chunk else "a",
            index=False,
            header=first_chunk,
        )

        total_rows += len(chunk)

        first_chunk = False


    # --------------------------------------------------------
    # COMPLETION MESSAGE
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING COMPLETED")
    print("=" * 60)

    print(f"Rows processed : {total_rows:,}")
    print(f"Saved to       : {ENRICHED_CSV_FILE}")

    print("=" * 60)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    create_enriched_dataset()