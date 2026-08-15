"""
feature_engineering.py
----------------------

Step 4 of the AML Fraud Analytics ETL pipeline.

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


def add_features(chunk):
    """
    Add AML and fraud-related analytical features to a dataframe chunk.

    The risk score used in this project is a heuristic analytical score
    for prioritization. It is not a validated production AML model.
    """

    # 1. Fraud status
    chunk["fraud_status"] = (
        chunk["isFraud"]
        .map(
            {
                0: "Legitimate",
                1: "Fraud",
            }
        )
        .fillna("Unknown")
    )

    # 2. Large transaction flag
    chunk["is_large_transaction"] = (
        chunk["amount"] >= LARGE_TRANSACTION_THRESHOLD
    ).astype("int8")

    # 3. Very large transaction flag
    chunk["is_very_large_transaction"] = (
        chunk["amount"] >= VERY_LARGE_TRANSACTION_THRESHOLD
    ).astype("int8")

    # 4. Near-threshold transaction proxy
    #
    # This does not detect true structuring behavior.
    # It only identifies transactions within a configured
    # near-threshold amount range for analytical review.
    chunk["structuring_proxy_flag"] = (
        chunk["amount"].between(
            STRUCTURING_LOWER_LIMIT,
            STRUCTURING_UPPER_LIMIT,
            inclusive="left",
        )
    ).astype("int8")

    # 5. Origin account emptied
    #
    # Sender had funds before the transaction and
    # the resulting balance became zero.
    chunk["origin_account_emptied"] = (
        (chunk["oldbalanceOrg"] > 0)
        & (chunk["newbalanceOrig"] == 0)
        & (chunk["amount"] > 0)
    ).astype("int8")

    # 6. Destination was empty
    #
    # Receiving account had zero balance before the transaction.
    chunk["destination_was_empty"] = (
        (chunk["oldbalanceDest"] == 0)
        & (chunk["amount"] > 0)
    ).astype("int8")

    # 7. Origin balance mismatch
    #
    # Expected:
    # old sender balance - amount = new sender balance
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

    # 8. Destination balance mismatch
    #
    # Expected:
    # old receiver balance + amount = new receiver balance
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

    # 9. Transaction-type analytical flag
    #
    # The cleaned dataset is focused on TRANSFER and CASH_OUT.
    chunk["high_risk_transaction_type"] = (
        chunk["type"].isin(
            [
                "TRANSFER",
                "CASH_OUT",
            ]
        )
    ).astype("int8")

    # 10. Hour of day
    #
    # PaySim step represents an hourly simulation step.
    chunk["hour_of_day"] = (
        (chunk["step"] - 1) % 24
    ).astype("int8")

    # 11. Day number
    chunk["day_number"] = (
        ((chunk["step"] - 1) // 24) + 1
    ).astype("int16")

    # 12. Heuristic risk score
    #
    # Large and very-large flags are intentionally cumulative.
    # Therefore, a very large transaction receives both weights.
    #
    # The structuring proxy and transaction-type flag are retained
    # for investigation and reporting but are not used directly
    # in the score to avoid overstating weak or population-wide signals.
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

    # 13. Risk level
    #
    # Low:    0-19
    # Medium: 20-49
    # High:   50-100
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
        include_lowest=True,
    )

    return chunk


def create_enriched_dataset():
    """
    Read the cleaned AML dataset in chunks,
    apply feature engineering,
    and save the enriched dataset.
    """

    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)

    print(f"Input file  : {CLEANED_CSV_FILE}")
    print(f"Output file : {ENRICHED_CSV_FILE}")
    print(f"Chunk size  : {CHUNK_SIZE:,}")

    ENRICHED_CSV_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Remove previous output before rebuilding
    if ENRICHED_CSV_FILE.exists():
        print("\nRemoving previous enriched dataset...")
        ENRICHED_CSV_FILE.unlink()

    total_rows = 0
    first_chunk = True

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

        chunk = add_features(chunk)

        chunk.to_csv(
            ENRICHED_CSV_FILE,
            mode="w" if first_chunk else "a",
            index=False,
            header=first_chunk,
        )

        total_rows += len(chunk)
        first_chunk = False

    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING COMPLETED")
    print("=" * 60)

    print(f"Rows processed : {total_rows:,}")
    print(f"Saved to       : {ENRICHED_CSV_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    create_enriched_dataset()