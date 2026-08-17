# AML Fraud Analytics & Transaction Monitoring

A data analytics project focused on transforming a large transaction dataset into an investigation-ready analytical layer using **Python, fraud/AML risk indicators, exploratory data analysis, and Power BI**.

The project focuses primarily on **CASH_OUT** and **TRANSFER** transactions, where confirmed fraudulent activity is concentrated in the source dataset.

After transformation and enrichment, the analytical population contains approximately **2.77 million transactions**.

This repository contains the Python analytics pipeline, fraud and risk-indicator logic, Power BI dashboard screenshots, and an executive case-study presentation.

---

## Business Problem

Transaction-monitoring teams must identify a relatively small number of potentially high-risk transactions within millions of legitimate transactions.

The challenge is not simply detecting high-value activity, but combining transaction characteristics and behavioral risk indicators to identify activity that warrants further investigation.

This project addresses that problem by transforming raw transaction data into an investigation-ready analytical layer and interactive Power BI dashboards that support risk-based transaction monitoring and investigation prioritization.

---

## Why This Project

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

- Approximately **2.77M transactions** in the analyzed population
- Approximately **8.21K confirmed fraud cases**
- Approximately **$12.06B confirmed fraud exposure**
- Approximately **1.20M large-value transactions flagged**
- Approximately **8.02K structuring-related alerts**
- End-to-end Python ETL and analytical pipeline
- Interactive Power BI executive and investigation dashboards
- Reproducible validation and analytical reporting workflow

---

## Dashboards

### Executive Overview

Portfolio-level monitoring view covering:

- Total transaction volume
- Confirmed fraud cases
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

## Key Findings

Confirmed fraud is concentrated almost entirely within **CASH_OUT** and **TRANSFER** transactions in the analyzed source data.

Although confirmed fraud represents only approximately **0.30% of the analyzed transaction population**, the associated monetary exposure is significant. This demonstrates why transaction-monitoring programs should consider both transaction counts and financial exposure.

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

## How It Works

```text
Raw Transaction Data
        |
        v
Extraction
        |
        v
Cleaning & Transformation
        |
        v
Risk Indicator Engineering
        |
        v
Validation
        |
        v
Exploratory Data Analysis
        |
        v
Power BI Dashboard
        |
        v
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
| `run_pipeline.py` | Runs the end-to-end analytical pipeline |

---

## Risk Indicators

The analytical layer combines transaction value, account-balance behavior, and transaction characteristics to prioritize activity for investigation.

| Risk Indicator | Investigation Rationale |
|---|---|
| **High-risk transaction type** | Highlights CASH_OUT and TRANSFER activity, where confirmed fraud is concentrated in the analyzed population |
| **Large transaction** | Flags transactions exceeding the defined large-value threshold for additional review |
| **Very large transaction** | Identifies exceptionally high-value transactions that may represent elevated financial exposure |
| **Origin account emptied** | Detects transactions where the originating account balance falls to zero after funds are transferred |
| **Destination was empty** | Identifies destination accounts with no prior balance before receiving funds |
| **Balance mismatch** | Detects inconsistencies between expected and actual account balances |
| **Structuring proxy** | Flags transaction behavior that may resemble structuring patterns and warrant further investigation |

> **Important:** These indicators are investigative signals, not automatic evidence of fraud or money laundering. They should be assessed alongside transaction history, customer context, and other relevant KYC/CDD information.

---

## Project Structure

```text
AML-Fraud-Transaction-Monitoring/
│
├── src/                              # Core Python analytics pipeline
│   ├── config.py                     # Project paths and configuration
│   ├── extract.py                    # Source data extraction
│   ├── transform.py                  # Data cleaning and transformation
│   ├── feature_engineering.py        # Fraud/AML risk-indicator engineering
│   ├── validation.py                 # Data and metric validation
│   └── eda.py                        # Exploratory data analysis
│
├── data/                             # Dataset structure (data files excluded)
│   ├── raw/
│   ├── cleaned/
│   ├── enriched/
│   └── reports/
│
├── screenshots/                      # Power BI dashboard previews
│   ├── executive_overview.png
│   └── investigation_detail.png
│
├── presentation/                     # Executive case-study presentation
│
├── run_pipeline.py                   # End-to-end pipeline runner
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
├── LICENSE                           # MIT License
└── .gitignore                        # Git exclusion rules
```

> **Note:** The raw, cleaned, enriched, and generated datasets are excluded from the repository because of file-size constraints. The Power BI `.pbix` file is also maintained locally; dashboard screenshots are provided above for portfolio review.

---

## Technology Stack

### Python

- pandas
- NumPy

### Data Visualization

- Microsoft Power BI

### Development

- Visual Studio Code
- Git
- GitHub

### Analytics

- Data cleaning
- ETL
- Exploratory data analysis
- Feature engineering
- Fraud analytics
- Transaction monitoring
- Risk segmentation

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/srinivassuresh975-afk/AML-Fraud-Transaction-Monitoring.git
cd AML-Fraud-Transaction-Monitoring
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the Source Dataset

Place the source transaction CSV inside:

```text
data/raw/
```

Verify that the source file path configured in:

```text
src/config.py
```

matches the dataset location.

### 4. Run the Pipeline

```bash
python run_pipeline.py
```

Individual scripts inside `src/` can also be executed separately when testing or reviewing a specific stage of the pipeline.

---

## Analytical Outputs

The pipeline generates analytical reporting outputs under:

```text
data/reports/
```

Including:

```text
aml_summary.csv
transaction_type_summary.csv
risk_level_summary.csv
red_flag_summary.csv
```

These generated files are excluded from Git because they can be reproduced by running the pipeline.

---

## Notes & Limitations

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

## Future Improvements

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