"""
config.py
---------

Central configuration for the AML Fraud Analytics pipeline.
"""

from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FOLDER = PROJECT_ROOT / "data"

RAW_DATA_FOLDER = DATA_FOLDER / "raw"
CLEANED_DATA_FOLDER = DATA_FOLDER / "cleaned"
ENRICHED_DATA_FOLDER = DATA_FOLDER / "enriched"
REPORTS_FOLDER = DATA_FOLDER / "reports"

# Create output folders if missing
CLEANED_DATA_FOLDER.mkdir(parents=True, exist_ok=True)
ENRICHED_DATA_FOLDER.mkdir(parents=True, exist_ok=True)
REPORTS_FOLDER.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# INPUT / OUTPUT FILES
# --------------------------------------------------

RAW_CSV_FILE = (
    RAW_DATA_FOLDER
    / "PS_20174392719_1491204439457_log.csv"
)

CLEANED_CSV_FILE = (
    CLEANED_DATA_FOLDER
    / "aml_transactions_cleaned.csv"
)

ENRICHED_CSV_FILE = (
    ENRICHED_DATA_FOLDER
    / "aml_transactions_enriched.csv"
)

# --------------------------------------------------
# PIPELINE SETTINGS
# --------------------------------------------------

CHUNK_SIZE = 500_000

# Transaction types where confirmed fraud is present
FRAUD_RELEVANT_TYPES = [
    "TRANSFER",
    "CASH_OUT",
]

# ============================================================
# FEATURE ENGINEERING THRESHOLDS
# ============================================================

# Transaction amount thresholds
LARGE_TRANSACTION_THRESHOLD = 200000
VERY_LARGE_TRANSACTION_THRESHOLD = 500000

# Structuring / smurfing range
STRUCTURING_LOWER_LIMIT = 9000
STRUCTURING_UPPER_LIMIT = 10000