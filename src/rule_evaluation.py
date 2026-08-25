import pandas as pd
import numpy as np
from pathlib import Path


# =========================================================
# PATH SETUP
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENRICHED_DATA_FILE = (
    BASE_DIR
    / "data"
    / "enriched"
    / "aml_transactions_enriched.csv"
)

REPORT_DIR = BASE_DIR / "data" / "reports"

OUTPUT_FILE = REPORT_DIR / "rule_effectiveness.csv"

CHUNK_SIZE = 500_000


# =========================================================
# FRAUD LABEL
# =========================================================

FRAUD_CANDIDATES = [
    "isFraud",
    "is_fraud",
    "fraud",
    "Fraud",
]


# =========================================================
# ACTUAL RULE COLUMNS
# =========================================================

RULE_COLUMNS = {
    "Large Value Transaction":
        "is_large_transaction",

    "Very Large Transaction":
        "is_very_large_transaction",

    "Structuring Proxy":
        "structuring_proxy_flag",

    "Origin Account Emptied":
        "origin_account_emptied",

    "Destination Was Empty":
        "destination_was_empty",

    "Origin Balance Mismatch":
        "origin_balance_mismatch",

    "Destination Balance Mismatch":
        "destination_balance_mismatch",

    "High Risk Transaction Type":
        "high_risk_transaction_type",
}


TRUE_TOKENS = {
    "1",
    "true",
    "yes",
    "y",
    "fraud",
    "flagged",
    "high",
}


# =========================================================
# HELPERS
# =========================================================

def safe_divide(numerator, denominator):
    """
    Safely divide two numbers.
    Returns 0 if denominator is 0.
    """

    if denominator == 0:
        return 0.0

    return numerator / denominator


def to_bool_array(series: pd.Series) -> np.ndarray:
    """
    Convert rule flag columns into boolean numpy arrays.

    Supports:
    - numeric 0 / 1
    - True / False
    - common text representations
    """

    series = series.fillna(0)

    if series.dtype == object:

        normalized = (
            series
            .astype(str)
            .str.strip()
            .str.lower()
        )

        return normalized.isin(
            TRUE_TOKENS
        ).to_numpy()

    return (
        series
        .to_numpy(dtype=float)
        > 0
    )


def confusion_counts(
    flag: np.ndarray,
    fraud: np.ndarray
) -> tuple[int, int, int, int]:
    """
    Calculate TP, FP, FN and TN using numpy.

    Encoding:
    0 -> TN
    1 -> FN
    2 -> FP
    3 -> TP
    """

    codes = (
        flag.astype(np.int8) * 2
        + fraud.astype(np.int8)
    )

    counts = np.bincount(
        codes,
        minlength=4
    )

    tn = int(counts[0])
    fn = int(counts[1])
    fp = int(counts[2])
    tp = int(counts[3])

    return tp, fp, fn, tn


def initialize_counter():
    """
    Return an empty confusion-matrix counter.
    """

    return {
        "TP": 0,
        "FP": 0,
        "FN": 0,
        "TN": 0,
    }


def add_counts(
    storage: dict,
    rule_name: str,
    flag: np.ndarray,
    fraud: np.ndarray
):
    """
    Add confusion-matrix counts for one monitoring strategy.
    """

    tp, fp, fn, tn = confusion_counts(
        flag,
        fraud
    )

    storage[rule_name]["TP"] += tp
    storage[rule_name]["FP"] += fp
    storage[rule_name]["FN"] += fn
    storage[rule_name]["TN"] += tn


# =========================================================
# MAIN EVALUATION
# =========================================================

def evaluate_rules():

    print("=" * 90)
    print("AML FRAUD RULE EFFECTIVENESS & BACKTESTING")
    print("=" * 90)

    # -----------------------------------------------------
    # VALIDATE INPUT FILE
    # -----------------------------------------------------

    if not ENRICHED_DATA_FILE.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n"
            f"{ENRICHED_DATA_FILE}"
        )

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # GLOBAL STORAGE
    # -----------------------------------------------------

    totals = {}

    total_rows = 0
    total_fraud = 0

    fraud_column = None
    discovered = False

    available_rule_columns = {}

    # -----------------------------------------------------
    # DEFINE STRATEGIES
    # -----------------------------------------------------

    individual_rule_names = list(
        RULE_COLUMNS.keys()
    )

    combined_rule_names = [
        "2+ Risk Indicators",
        "3+ Risk Indicators",
        "4+ Risk Indicators",

        "Risk Score >= 20",
        "Risk Score >= 30",
        "Risk Score >= 40",
        "Risk Score >= 50",
        "Risk Score >= 60",

        "Origin Emptied + Destination Empty",
        "Origin Emptied + Large Value",
        "Destination Empty + Large Value",
        "Destination Mismatch + Large Value",
        "Origin Emptied + Destination Empty + Large Value",
        "Very Large + Destination Empty",
        "Very Large + Origin Emptied",
    ]

    all_rule_names = (
        individual_rule_names
        + combined_rule_names
    )

    for rule_name in all_rule_names:

        totals[
            rule_name
        ] = initialize_counter()

    print("\nReading enriched dataset in chunks...\n")

    # =====================================================
    # READ DATA
    # =====================================================

    for chunk_number, chunk in enumerate(

        pd.read_csv(
            ENRICHED_DATA_FILE,
            chunksize=CHUNK_SIZE
        ),

        start=1,
    ):

        total_rows += len(chunk)

        # -------------------------------------------------
        # IDENTIFY FRAUD LABEL
        # -------------------------------------------------

        if fraud_column is None:

            for candidate in FRAUD_CANDIDATES:

                if candidate in chunk.columns:

                    fraud_column = candidate
                    break

            if fraud_column is None:

                raise ValueError(
                    "Could not identify fraud label column."
                )

        fraud = (
            chunk[fraud_column]
            .fillna(0)
            .to_numpy(dtype=int)
            == 1
        )

        total_fraud += int(
            fraud.sum()
        )

        # -------------------------------------------------
        # DISCOVER AVAILABLE RULE COLUMNS
        # -------------------------------------------------

        if not discovered:

            discovered = True

            print("Columns found:")
            print("-" * 90)

            for col in chunk.columns:
                print(col)

            print("-" * 90)

            print("\nDetected individual rule columns:")
            print("-" * 90)

            for (
                rule_name,
                column_name
            ) in RULE_COLUMNS.items():

                if column_name in chunk.columns:

                    available_rule_columns[
                        rule_name
                    ] = column_name

                    print(
                        f"{rule_name:<40}"
                        f" -> "
                        f"{column_name}"
                    )

                else:

                    print(
                        f"WARNING: Missing "
                        f"{column_name}"
                    )

            print("-" * 90)

            print(
                f"Detected rules: "
                f"{len(available_rule_columns)} "
                f"of "
                f"{len(RULE_COLUMNS)}"
            )

        # =================================================
        # BUILD BOOLEAN FLAGS
        # =================================================

        flags = {}

        for (
            rule_name,
            column_name
        ) in available_rule_columns.items():

            flags[
                rule_name
            ] = to_bool_array(
                chunk[column_name]
            )

        # =================================================
        # INDIVIDUAL RULE EVALUATION
        # =================================================

        for rule_name, flag in flags.items():

            add_counts(
                totals,
                rule_name,
                flag,
                fraud
            )

        # =================================================
        # MULTI-INDICATOR COUNT
        #
        # IMPORTANT:
        # High Risk Transaction Type is intentionally
        # excluded because the dataset is already filtered
        # to high-risk transaction types.
        # =================================================

        indicator_arrays = [
            flag.astype(np.int8)
            for rule_name, flag in flags.items()
            if rule_name != "High Risk Transaction Type"
        ]

        if indicator_arrays:

            indicator_count = np.sum(
                indicator_arrays,
                axis=0
            )

            multi_indicator_rules = {

                "2+ Risk Indicators":
                    indicator_count >= 2,

                "3+ Risk Indicators":
                    indicator_count >= 3,

                "4+ Risk Indicators":
                    indicator_count >= 4,
            }

            for (
                rule_name,
                flag
            ) in multi_indicator_rules.items():

                add_counts(
                    totals,
                    rule_name,
                    flag,
                    fraud
                )

        # =================================================
        # RISK SCORE THRESHOLDS
        #
        # Actual score values are on a 0-85 scale,
        # not 0-5.
        # =================================================

        if "risk_score" in chunk.columns:

            risk_score = pd.to_numeric(
                chunk["risk_score"],
                errors="coerce"
            ).fillna(0).to_numpy()

            score_rules = {

                "Risk Score >= 20":
                    risk_score >= 20,

                "Risk Score >= 30":
                    risk_score >= 30,

                "Risk Score >= 40":
                    risk_score >= 40,

                "Risk Score >= 50":
                    risk_score >= 50,

                "Risk Score >= 60":
                    risk_score >= 60,
            }

            for (
                rule_name,
                flag
            ) in score_rules.items():

                add_counts(
                    totals,
                    rule_name,
                    flag,
                    fraud
                )

        # =================================================
        # SELECTED RULE COMBINATIONS
        # =================================================

        required = {
            "origin":
                flags.get(
                    "Origin Account Emptied"
                ),

            "dest_empty":
                flags.get(
                    "Destination Was Empty"
                ),

            "large":
                flags.get(
                    "Large Value Transaction"
                ),

            "very_large":
                flags.get(
                    "Very Large Transaction"
                ),

            "dest_mismatch":
                flags.get(
                    "Destination Balance Mismatch"
                ),
        }

        # -------------------------------------------------
        # ORIGIN EMPTIED + DESTINATION EMPTY
        # -------------------------------------------------

        if (
            required["origin"] is not None
            and required["dest_empty"] is not None
        ):

            flag = (
                required["origin"]
                & required["dest_empty"]
            )

            add_counts(
                totals,
                "Origin Emptied + Destination Empty",
                flag,
                fraud
            )

        # -------------------------------------------------
        # ORIGIN EMPTIED + LARGE VALUE
        # -------------------------------------------------

        if (
            required["origin"] is not None
            and required["large"] is not None
        ):

            flag = (
                required["origin"]
                & required["large"]
            )

            add_counts(
                totals,
                "Origin Emptied + Large Value",
                flag,
                fraud
            )

        # -------------------------------------------------
        # DESTINATION EMPTY + LARGE VALUE
        # -------------------------------------------------

        if (
            required["dest_empty"] is not None
            and required["large"] is not None
        ):

            flag = (
                required["dest_empty"]
                & required["large"]
            )

            add_counts(
                totals,
                "Destination Empty + Large Value",
                flag,
                fraud
            )

        # -------------------------------------------------
        # DESTINATION MISMATCH + LARGE VALUE
        # -------------------------------------------------

        if (
            required["dest_mismatch"] is not None
            and required["large"] is not None
        ):

            flag = (
                required["dest_mismatch"]
                & required["large"]
            )

            add_counts(
                totals,
                "Destination Mismatch + Large Value",
                flag,
                fraud
            )

        # -------------------------------------------------
        # ORIGIN + DESTINATION + LARGE VALUE
        # -------------------------------------------------

        if (
            required["origin"] is not None
            and required["dest_empty"] is not None
            and required["large"] is not None
        ):

            flag = (
                required["origin"]
                & required["dest_empty"]
                & required["large"]
            )

            add_counts(
                totals,
                "Origin Emptied + Destination Empty + Large Value",
                flag,
                fraud
            )

        # -------------------------------------------------
        # VERY LARGE + DESTINATION EMPTY
        # -------------------------------------------------

        if (
            required["very_large"] is not None
            and required["dest_empty"] is not None
        ):

            flag = (
                required["very_large"]
                & required["dest_empty"]
            )

            add_counts(
                totals,
                "Very Large + Destination Empty",
                flag,
                fraud
            )

        # -------------------------------------------------
        # VERY LARGE + ORIGIN EMPTIED
        # -------------------------------------------------

        if (
            required["very_large"] is not None
            and required["origin"] is not None
        ):

            flag = (
                required["very_large"]
                & required["origin"]
            )

            add_counts(
                totals,
                "Very Large + Origin Emptied",
                flag,
                fraud
            )

        print(
            f"Processed chunk "
            f"{chunk_number:,} "
            f"| cumulative rows: "
            f"{total_rows:,}"
        )

    # =====================================================
    # BUILD FINAL METRICS
    # =====================================================

    results = []

    for (
        rule_name,
        counts
    ) in totals.items():

        tp = counts["TP"]
        fp = counts["FP"]
        fn = counts["FN"]
        tn = counts["TN"]

        alerts = tp + fp

        # Skip strategies that never executed
        if (
            alerts == 0
            and tp == 0
            and fp == 0
            and fn == 0
            and tn == 0
        ):
            continue

        precision = safe_divide(
            tp,
            tp + fp
        )

        recall = safe_divide(
            tp,
            tp + fn
        )

        f1_score = safe_divide(
            2 * precision * recall,
            precision + recall
        )

        false_positive_rate = safe_divide(
            fp,
            fp + tn
        )

        false_alert_rate = safe_divide(
            fp,
            alerts
        )

        specificity = safe_divide(
            tn,
            tn + fp
        )

        alert_rate = safe_divide(
            alerts,
            total_rows
        )

        results.append({

            "Risk Indicator":
                rule_name,

            "Total Alerts":
                alerts,

            "True Positives":
                tp,

            "False Positives":
                fp,

            "False Negatives":
                fn,

            "True Negatives":
                tn,

            "Precision":
                round(
                    precision,
                    6
                ),

            "Recall":
                round(
                    recall,
                    6
                ),

            "F1 Score":
                round(
                    f1_score,
                    6
                ),

            "Precision %":
                round(
                    precision * 100,
                    2
                ),

            "Recall %":
                round(
                    recall * 100,
                    2
                ),

            "False Positive Rate %":
                round(
                    false_positive_rate * 100,
                    2
                ),

            "False Alert %":
                round(
                    false_alert_rate * 100,
                    2
                ),

            "Specificity %":
                round(
                    specificity * 100,
                    2
                ),

            "Alert Rate %":
                round(
                    alert_rate * 100,
                    2
                ),
        })

    results_df = pd.DataFrame(
        results
    )

    # =====================================================
    # FALSE POSITIVE REDUCTION VS LARGE VALUE BASELINE
    # =====================================================

    baseline_rows = results_df[
        results_df["Risk Indicator"]
        == "Large Value Transaction"
    ]

    if not baseline_rows.empty:

        baseline_fp = int(
            baseline_rows.iloc[0][
                "False Positives"
            ]
        )

        baseline_alerts = int(
            baseline_rows.iloc[0][
                "Total Alerts"
            ]
        )

        results_df[
            "FP Reduction vs Large Value %"
        ] = results_df[
            "False Positives"
        ].apply(
            lambda fp: round(
                safe_divide(
                    baseline_fp - fp,
                    baseline_fp
                ) * 100,
                2
            )
        )

        results_df[
            "Alert Reduction vs Large Value %"
        ] = results_df[
            "Total Alerts"
        ].apply(
            lambda alerts: round(
                safe_divide(
                    baseline_alerts - alerts,
                    baseline_alerts
                ) * 100,
                2
            )
        )

    else:

        results_df[
            "FP Reduction vs Large Value %"
        ] = 0.0

        results_df[
            "Alert Reduction vs Large Value %"
        ] = 0.0

    # =====================================================
    # RANKING
    # =====================================================

    results_df = (
        results_df
        .sort_values(
            by=[
                "F1 Score",
                "Recall %",
                "Precision %",
            ],
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )

    results_df.insert(
        0,
        "Rank",
        range(
            1,
            len(results_df) + 1
        )
    )

    # =====================================================
    # SAVE CSV
    # =====================================================

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    fraud_rate = safe_divide(
        total_fraud,
        total_rows
    ) * 100

    print("\n")
    print("=" * 90)
    print("DATASET SUMMARY")
    print("=" * 90)

    print(
        f"Total Transactions : "
        f"{total_rows:,}"
    )

    print(
        f"Confirmed Fraud    : "
        f"{total_fraud:,}"
    )

    print(
        f"Overall Fraud Rate : "
        f"{fraud_rate:.4f}%"
    )

    # =====================================================
    # EFFECTIVENESS TABLE
    # =====================================================

    print("\n")
    print("=" * 90)
    print("RULE & COMBINATION EFFECTIVENESS")
    print("=" * 90)

    display_columns = [
        "Rank",
        "Risk Indicator",
        "Total Alerts",
        "True Positives",
        "False Positives",
        "False Negatives",
        "Precision %",
        "Recall %",
        "F1 Score",
        "FP Reduction vs Large Value %",
    ]

    print(
        results_df[
            display_columns
        ].to_string(
            index=False
        )
    )

    # =====================================================
    # BEST F1 STRATEGY
    # =====================================================

    best_f1 = results_df.iloc[0]

    print("\n")
    print("=" * 90)
    print("BEST F1 STRATEGY")
    print("=" * 90)

    print(
        f"Strategy      : "
        f"{best_f1['Risk Indicator']}"
    )

    print(
        f"Total Alerts  : "
        f"{int(best_f1['Total Alerts']):,}"
    )

    print(
        f"True Fraud    : "
        f"{int(best_f1['True Positives']):,}"
    )

    print(
        f"False Alerts  : "
        f"{int(best_f1['False Positives']):,}"
    )

    print(
        f"Missed Fraud  : "
        f"{int(best_f1['False Negatives']):,}"
    )

    print(
        f"Precision     : "
        f"{best_f1['Precision %']:.2f}%"
    )

    print(
        f"Recall        : "
        f"{best_f1['Recall %']:.2f}%"
    )

    print(
        f"F1 Score      : "
        f"{best_f1['F1 Score']:.4f}"
    )

    print(
        f"FP Reduction  : "
        f"{best_f1['FP Reduction vs Large Value %']:.2f}%"
    )

    # =====================================================
    # BEST HIGH-RECALL STRATEGY
    # =====================================================

    high_recall = results_df[
        results_df["Recall %"] >= 60
    ]

    if not high_recall.empty:

        high_recall = (
            high_recall
            .sort_values(
                by=[
                    "Precision %",
                    "F1 Score",
                ],
                ascending=False
            )
        )

        best_high_recall = (
            high_recall.iloc[0]
        )

        print("\n")
        print("=" * 90)
        print("BEST STRATEGY WITH RECALL >= 60%")
        print("=" * 90)

        print(
            f"Strategy      : "
            f"{best_high_recall['Risk Indicator']}"
        )

        print(
            f"Total Alerts  : "
            f"{int(best_high_recall['Total Alerts']):,}"
        )

        print(
            f"True Fraud    : "
            f"{int(best_high_recall['True Positives']):,}"
        )

        print(
            f"False Alerts  : "
            f"{int(best_high_recall['False Positives']):,}"
        )

        print(
            f"Missed Fraud  : "
            f"{int(best_high_recall['False Negatives']):,}"
        )

        print(
            f"Precision     : "
            f"{best_high_recall['Precision %']:.2f}%"
        )

        print(
            f"Recall        : "
            f"{best_high_recall['Recall %']:.2f}%"
        )

        print(
            f"F1 Score      : "
            f"{best_high_recall['F1 Score']:.4f}"
        )

        print(
            f"FP Reduction  : "
            f"{best_high_recall['FP Reduction vs Large Value %']:.2f}%"
        )

    # =====================================================
    # BUSINESS INTERPRETATION
    # =====================================================

    print("\n")
    print("=" * 90)
    print("BUSINESS INTERPRETATION")
    print("=" * 90)

    print(
        "Precision = of all alerts generated, "
        "how many were actual fraud."
    )

    print(
        "Recall = of all confirmed fraud cases, "
        "how many were detected."
    )

    print(
        "False-positive reduction = how much investigative "
        "noise was removed versus the Large Value baseline."
    )

    print()

    print(
        "High Risk Transaction Type is evaluated separately "
        "but excluded from multi-indicator counts because the "
        "analysis dataset already contains only TRANSFER and "
        "CASH_OUT transactions."
    )

    print()

    print(
        "The strongest operational strategy is not simply "
        "the highest single metric. It should balance fraud "
        "capture, alert quality, and investigation workload."
    )

    # =====================================================
    # OUTPUT LOCATION
    # =====================================================

    print("\n")
    print("=" * 90)
    print("REPORT SAVED")
    print("=" * 90)

    print(
        OUTPUT_FILE
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    evaluate_rules()