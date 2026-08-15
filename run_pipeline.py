"""
run_pipeline.py
---------------

Master pipeline runner for the AML Fraud Analytics project.

Pipeline:
1. Extract / inspect raw dataset
2. Validate raw dataset
3. Clean / transform dataset
4. Feature engineering
5. EDA and reporting
"""

from src.extract import load_sample, count_rows
from src.validation import validate_dataset
from src.transform import clean_dataset
from src.feature_engineering import create_enriched_dataset
from src.eda import run_eda


def run_pipeline():

    print("\n" + "=" * 60)
    print("AML FRAUD ANALYTICS - ETL PIPELINE")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1 - EXTRACT / INSPECT
    # --------------------------------------------------

    print("\n[1/5] EXTRACT / DATA INSPECTION")
    print("-" * 60)

    total_rows = count_rows()
    print(f"Raw dataset rows: {total_rows:,}")

    print("\nSample records:")
    sample = load_sample(5)
    print(sample)


    # --------------------------------------------------
    # STEP 2 - VALIDATION
    # --------------------------------------------------

    print("\n[2/5] DATA VALIDATION")
    print("-" * 60)

    validate_dataset()


    # --------------------------------------------------
    # STEP 3 - TRANSFORM / CLEAN
    # --------------------------------------------------

    print("\n[3/5] DATA CLEANING")
    print("-" * 60)

    clean_dataset()


    # --------------------------------------------------
    # STEP 4 - FEATURE ENGINEERING
    # --------------------------------------------------

    print("\n[4/5] FEATURE ENGINEERING")
    print("-" * 60)

    create_enriched_dataset()


    # --------------------------------------------------
    # STEP 5 - EDA / REPORTING
    # --------------------------------------------------

    print("\n[5/5] EDA & REPORTING")
    print("-" * 60)

    run_eda()


    # --------------------------------------------------
    # PIPELINE COMPLETE
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()