# AML Fraud Analytics & Transaction Monitoring

A data analytics project focused on transforming a large transaction dataset into an investigation-ready analytical layer using Python, fraud/AML risk indicators, exploratory analysis, and Power BI.

The project focuses primarily on **CASH_OUT** and **TRANSFER** transactions, where confirmed fraudulent activity is concentrated in the source dataset.

After transformation and enrichment, the analytical population contains approximately **2.77 million transactions**.

This repository contains the Python analytics pipeline, fraud and risk-indicator logic, Power BI dashboard screenshots, and an executive case-study presentation.

---

## Why this project

Reviewing millions of transactions manually is not practical for a fraud or AML investigation team.

The objective of this project is to demonstrate how transaction data can be cleaned, transformed, enriched with behavioral risk indicators, and converted into an investigation-prioritization layer.

The analysis considers indicators such as:

- High-risk transaction types
- Large-value transactions
- Very large-value transactions
- Origin accounts drained after transactions
- Previously empty destination accounts receiving funds
- Origin balance mismatches
- Destination balance mismatches
- Structuring-like transaction patterns

These indicators are designed to support investigation prioritization and should not be interpreted as proof of fraudulent activity on their own.

---

## Highlights

- **2.77M** transactions in the analyzed population
- **8.21K** confirmed fraud cases (~0.30% of transactions)
- Approximately **$12.06B** in confirmed fraud exposure
- Approximately **1.20M** large-value transactions flagged
- Approximately **8.02K** structuring-related alerts
- End-to-end Python ETL and analytical pipeline
- Interactive Power BI executive and investigation dashboards

---

## Dashboards

### Executive Overview

Portfolio-level monitoring view covering:

- Total transaction volume
- Confirmed fraud transactions
- Fraud exposure
- Fraud percentage
- Large transactions
- Transaction-type distribution
- Fraud vs legitimate transactions
- Risk-level distribution
- Transaction activity over time

![Executive Overview](screenshots/executive_overview.png)

### Investigation Details

Investigation-focused view designed to help analysts review suspicious transactions and prioritize higher-risk activity.

![Investigation Details](screenshots/investigation_detail.png)

---

## Key findings

Confirmed fraud is concentrated almost entirely within **CASH_OUT** and **TRANSFER** transactions.

Although confirmed fraud represents only approximately **0.30% of transaction volume**, the associated monetary exposure is significant. This demonstrates why transaction-monitoring programs should consider both transaction counts and financial exposure.

Large transaction value alone is not sufficient to classify suspicious activity because high-value transactions can also occur within legitimate activity.

Combining transaction value with behavioral indicators provides a stronger investigation-prioritization framework.

Examples include:

- Origin account drained after the transaction
- Previously empty destination account receiving funds
- Balance inconsistencies
- Structuring-like transaction behavior
- High-risk transaction types

These indicators are treated as signals requiring additional review rather than automatic fraud conclusions.

---

## How it works

```text
Raw Transaction Data
        ↓
Extraction
        ↓
Cleaning & Transformation
        ↓
Risk Indicator Engineering
        ↓
Validation
        ↓
Exploratory Data Analysis
        ↓
Power BI Dashboard
        ↓
Investigation & Review
```

Each major analytical stage is separated into its own Python module.

| Script | Purpose |
|---|---|
| `extract.py` | Reads and inspects the source transaction dataset |
| `transform.py` | Cleans the data and creates the analytical population |
| `feature_engineering.py` | Creates behavioral and transaction risk indicators |
| `validation.py` | Validates processed data and key fraud metrics |
| `eda.py` | Generates analytical summaries and reporting outputs |
| `config.py` | Stores reusable project paths and configuration |
| `run_pipeline.py` | Runs the analytical pipeline |

---

## Risk indicators

The feature-engineering stage creates several indicators that can assist investigation prioritization.

Examples include:

### High-risk transaction type

Identifies transaction categories associated with higher fraud exposure in the analyzed dataset.

### Large transaction

Flags transactions exceeding the defined large-value threshold.

### Very large transaction

Identifies transactions with exceptionally high monetary value.

### Origin account emptied

Flags cases where the originating account balance falls to zero following a transaction.

### Destination was empty

Identifies destination accounts with no prior balance before receiving funds.

### Balance mismatch

Detects inconsistencies between expected and reported account balances.

### Structuring proxy

Identifies transaction behavior that may resemble structuring patterns and therefore warrants additional review.

These indicators should be interpreted together with transaction history and customer context.

---

## Project structure

```text
AML-Fraud-Transaction-Monitoring/
│
├── dashboard/
│
├── data/
│
├── docs/
│
├── logs/
│
├── notebooks/
│
├── presentation/
│
├── screenshots/
│   ├── executive_overview.png
│   └── investigation_detail.png
│
├── sql/
│
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── feature_engineering.py
│   ├── validation.py
│   └── eda.py
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run_pipeline.py
```

Raw and generated datasets are not stored in the repository because of their size.

---

## Technology stack

**Python**

- pandas
- NumPy

**Data Visualization**

- Microsoft Power BI

**Development**

- Visual Studio Code
- Git
- GitHub

**Analytics**

- Data cleaning
- ETL
- Exploratory data analysis
- Feature engineering
- Fraud analytics
- Transaction monitoring
- Risk segmentation

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/srinivassuresh975-afk/AML-Fraud-Transaction-Monitoring.git
cd AML-Fraud-Transaction-Monitoring
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the source dataset

Place the source transaction CSV inside:

```text
data/raw/
```

Verify that the source file path in:

```text
src/config.py
```

matches the dataset location.

### 4. Run the pipeline

```bash
python run_pipeline.py
```

Individual scripts inside `src/` can also be executed separately when testing or reviewing a specific stage of the pipeline.

---

## Requirements

The project currently uses:

```text
pandas>=2.0.0
numpy>=1.24.0
```

These dependencies are defined in:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## Notes & limitations

The risk indicators in this project are intended to support transaction-monitoring and investigation prioritization.

They should **not** be interpreted as automatic determinations of fraud, money laundering, or other financial crime.

In a production AML/fraud environment, an alert would require additional investigation involving factors such as:

- Customer profile
- Transaction history
- Counterparty behavior
- Source and destination of funds
- Expected account activity
- Customer risk rating
- Additional KYC/CDD information
- Investigator judgment

The complete raw dataset and generated analytical datasets are excluded from this repository because of their size.

The Power BI `.pbix` file is also not included; dashboard screenshots are provided to demonstrate the analytical output.

---

## Future improvements

Potential enhancements include:

- Backtesting the risk logic against additional historical datasets
- Converting static structuring checks into rolling-window/velocity analysis
- Developing a calibrated transaction risk score
- Adding customer-level behavioral profiling
- Incorporating SQL-based analytical workflows
- Adding automated data-quality testing
- Adding model-based anomaly detection as a complementary analytical layer

---

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## Contact

**Srinivas Suresh**

For questions regarding the project, methodology, or analytical approach, feel free to open an issue through the repository.