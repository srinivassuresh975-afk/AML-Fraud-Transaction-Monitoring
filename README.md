# 🛡️ AML Fraud Analytics & Transaction Monitoring

> An end-to-end Data Analytics case study transforming large-scale financial transaction data into actionable AML and fraud intelligence using **Python, Pandas, feature engineering, exploratory data analysis, SQL concepts, and Power BI**.

This project simulates a real-world transaction-monitoring workflow: processing raw transaction data, engineering fraud-risk indicators, validating suspicious behavior, prioritizing transactions for investigation, and presenting management-level insights through an interactive Power BI dashboard.

---

## 📊 Dashboard Preview

### Executive Fraud Intelligence Dashboard

![AML Fraud Intelligence Dashboard](screenshots/executive_overview.png)

### Transaction Investigation Dashboard

![AML Case Investigation Dashboard](screenshots/investigation_detail.png)

---

## 🎯 Executive Summary

The objective of this project was to build an analytics-driven transaction-monitoring framework capable of identifying fraudulent activity, suspicious transaction behavior, high-risk transactions, and investigation priorities from a large financial transaction dataset.

The final analytical dataset contains approximately **2.77 million transactions**, focused on **CASH_OUT** and **TRANSFER** activity.

Key portfolio findings include:

- **2.77M** analyzed transactions
- **8.21K** confirmed fraudulent transactions
- Approximately **0.30%** overall fraud rate
- Approximately **12.06bn** in confirmed fraud exposure
- Approximately **1.20M** large-value transactions
- Approximately **8.02K** structuring alerts
- Confirmed fraud concentrated within **CASH_OUT** and **TRANSFER**

The project demonstrates how data analytics can support fraud-investigation teams by converting transaction-level data into prioritized risk intelligence.

---

## 💼 Business Problem

Financial institutions process millions of transactions, making manual transaction review impractical.

An effective monitoring framework therefore needs to answer several questions:

- Which transactions represent confirmed or elevated fraud risk?
- Which transaction behaviors should investigators prioritize?
- Which accounts contribute the greatest fraud exposure?
- Are there recognizable transaction patterns associated with fraudulent activity?
- How can millions of transactions be transformed into an investigation-ready queue?
- How can management monitor fraud exposure without reviewing transaction-level data?

This project was designed around those questions.

---

## 🎯 Project Objectives

The analysis focuses on:

- Detecting confirmed fraudulent transactions
- Identifying high-risk and large-value transactions
- Detecting potential structuring behavior
- Identifying accounts drained to zero after transactions
- Identifying transactions involving previously empty destination accounts
- Engineering transaction-level risk indicators
- Assigning transaction risk scores and risk levels
- Analyzing fraud by transaction type
- Analyzing fraud activity by hour of day
- Identifying origin accounts with significant fraud exposure
- Creating an investigation queue for transaction review
- Presenting executive-level fraud KPIs through Power BI

---

## 🏗️ Analytics Architecture

```text
Raw Transaction Data
        |
        ▼
┌─────────────────────┐
│   Data Extraction   │
│     extract.py      │
└─────────────────────┘
        |
        ▼
┌─────────────────────┐
│ Data Transformation │
│    transform.py     │
└─────────────────────┘
        |
        ▼
┌─────────────────────────┐
│   Feature Engineering   │
│ feature_engineering.py  │
└─────────────────────────┘
        |
        ▼
┌─────────────────────┐
│   Data Validation   │
│    validation.py    │
└─────────────────────┘
        |
        ▼
┌─────────────────────┐
│ Exploratory Analysis│
│       eda.py        │
└─────────────────────┘
        |
        ▼
┌─────────────────────┐
│   Power BI Model    │
└─────────────────────┘
        |
        ▼
Executive Dashboard + Investigation Queue


---

## 📂 Dataset Overview

The project analyzes a large-scale synthetic financial transaction dataset containing transaction-level information such as:

- Transaction type
- Transaction amount
- Origin account
- Origin account balance before and after the transaction
- Destination account
- Destination account balance before and after the transaction
- Fraud indicator

For the final analytical model, the dataset was narrowed to **CASH_OUT** and **TRANSFER** transactions because these transaction types contain the confirmed fraudulent activity relevant to the fraud-monitoring analysis.

After transformation and preparation, the analytical dataset contains approximately **2.77 million transactions**.

> **Note:** Large raw and processed datasets are excluded from this repository to keep the project lightweight and suitable for GitHub.

---

## ⚙️ Data Analytics Pipeline

The project follows a modular Python pipeline rather than performing all processing in a single script.

### 1. Data Extraction — `extract.py`

Responsible for accessing the source transaction dataset and performing initial inspection of the raw data.

Key activities include:

- Loading transaction data
- Inspecting sample records
- Checking dataset size
- Supporting chunk-based processing for large files

### 2. Data Transformation — `transform.py`

Transforms the raw transaction data into an analysis-ready dataset.

Key activities include:

- Removing duplicate records
- Handling missing values
- Filtering relevant transaction types
- Preparing the cleaned dataset for downstream analysis

### 3. Feature Engineering — `feature_engineering.py`

Creates analytical indicators used to identify potentially suspicious transaction behavior.

Examples include:

- Origin account drained to zero
- Previously empty destination account
- Large-value transaction indicators
- Potential structuring behavior
- Transaction risk indicators
- Risk scoring and risk categorization

### 4. Data Validation — `validation.py`

Performs validation checks on the transformed and enriched transaction data.

Validation helps confirm:

- Transaction volumes
- Fraud counts
- Fraud percentages
- Data consistency
- Relationship between engineered indicators and confirmed fraud

### 5. Exploratory Data Analysis — `eda.py`

Analyzes transaction and fraud behavior to identify patterns suitable for investigation and dashboard reporting.

### 6. Power BI

The prepared analytical dataset is loaded into Power BI for interactive analysis, KPI monitoring, fraud intelligence, and transaction investigation.

---

## 🚩 Fraud & AML Risk Indicators

Several transaction-level indicators were engineered to convert raw transaction records into more useful investigation signals.

| Risk Indicator | Analytical Purpose |
|---|---|
| Confirmed Fraud | Identifies transactions labelled as fraudulent in the source data |
| Account Drained to Zero | Highlights transactions where the origin balance becomes zero |
| Empty Destination Account | Identifies transactions involving destinations with no prior balance |
| Large-Value Transaction | Flags transactions exceeding the defined high-value threshold |
| Structuring Indicator | Identifies transaction behavior potentially consistent with transaction splitting |
| Risk Score | Combines transaction-level risk indicators |
| Risk Level | Categorizes transactions for easier investigation prioritization |

These indicators are analytical signals and should not independently be interpreted as evidence of money laundering or criminal activity.

---

## ⚠️ Risk-Based Investigation Approach

Instead of treating every transaction equally, the project uses engineered risk indicators to help prioritize transactions for review.

Transactions exhibiting multiple suspicious characteristics can be assigned greater analytical priority.

This enables a workflow similar to:

```text
Transaction
     ↓
Risk Indicators
     ↓
Risk Assessment
     ↓
Risk Level
     ↓
Investigation Queue
     ↓
Analyst Review
```

The purpose of this approach is to demonstrate how analytics can help investigators focus attention on higher-risk activity within a dataset containing millions of transactions.

---

## 🔎 Exploratory Data Analysis

Exploratory analysis was performed to understand transaction behavior and identify patterns associated with confirmed fraudulent activity.

The analysis examines areas including:

- Fraudulent vs legitimate transactions
- Fraud by transaction type
- Fraud exposure by transaction amount
- Transaction activity by hour of day
- High-risk transaction distribution
- Large-value transaction activity
- Structuring indicators
- Origin accounts with significant fraud exposure
- Relationships between engineered risk indicators and confirmed fraud

The resulting insights were used to determine which KPIs and investigation views should be presented in Power BI.

---

## 📊 Power BI Dashboard

The Power BI solution contains two primary analytical views.

### 1. Executive Fraud Intelligence Dashboard

Designed for management-level monitoring of fraud exposure and transaction risk.

Key KPIs include:

- Total Transactions
- Fraud Amount
- Fraud Transactions
- Fraud Rate
- Large-Value Transactions
- Structuring Alerts

Interactive slicers allow users to analyze the portfolio by relevant transaction and risk dimensions.

The dashboard also provides visual analysis of fraud distribution and transaction behavior.

### 2. Transaction Investigation Dashboard

Designed for transaction-level investigation and prioritization.

The investigation view enables users to:

- Filter suspicious transactions
- Review transaction risk levels
- Examine fraud indicators
- Analyze transaction amounts
- Review origin and destination account information
- Prioritize transactions requiring further investigation

Together, the two pages provide both **executive-level monitoring** and **analyst-level investigation capability**.

---

## 💡 Key Analytical Insights

The final analysis produced several notable findings:

- Approximately **2.77 million transactions** were included in the final analytical dataset.
- Approximately **8.21K transactions** were identified as confirmed fraud.
- The overall confirmed fraud rate was approximately **0.30%**.
- Confirmed fraud exposure totaled approximately **12.06bn**.
- Fraudulent activity in the analyzed dataset is concentrated within **CASH_OUT** and **TRANSFER** transaction types.
- Approximately **1.20M transactions** were classified as large-value transactions.
- Approximately **8.02K transactions** triggered the project's structuring indicator.
- Transaction-level behavioral indicators can be combined with confirmed fraud information to create a more focused investigation workflow.

These findings demonstrate why fraud monitoring should consider both transaction outcomes and behavioral risk indicators rather than relying on transaction volume alone.

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core data-processing and analytics language |
| Pandas | Data cleaning, transformation, feature engineering and analysis |
| Power BI | Interactive dashboard development and investigation reporting |
| DAX | Dashboard measures, KPIs and analytical calculations |
| SQL Concepts | Relational analysis concepts applied to the analytical workflow |
| Git | Version control |
| GitHub | Project documentation and portfolio hosting |
| VS Code | Development environment |

---

## 📁 Project Structure

```text
AML-Fraud-Analytics/
│
├── dashboard/
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── enriched/
│   └── reports/
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
│   ├── eda.py
│   ├── extract.py
│   ├── feature_engineering.py
│   ├── load.py
│   ├── transform.py
│   ├── utils.py
│   └── validation.py
│
├── .gitignore
├── README.md
└── run_pipeline.py
```

The modular structure separates extraction, transformation, feature engineering, validation, analysis, and reporting responsibilities.

---

## ▶️ Running the Project

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd AML-Fraud-Analytics
```

Ensure the required Python packages are installed.

The primary Python dependency used for transaction processing is:

```bash
pip install pandas
```

Place the source transaction dataset in the appropriate raw-data directory and verify the configured input path in `src/config.py`.

The complete pipeline can then be executed using:

```bash
python run_pipeline.py
```

Individual stages can also be executed separately during development or validation.

---

## 🔐 Data & Repository Considerations

The original transaction dataset and generated analytical datasets are large and are therefore not stored directly in this GitHub repository.

This repository focuses on the project's:

- Analytics methodology
- Python pipeline
- Feature-engineering logic
- Validation approach
- Power BI output
- Project documentation

This also prevents unnecessary duplication of large data files in version control.

---

## 📈 Skills Demonstrated

This project demonstrates practical application of:

- Data cleaning and transformation
- Large-dataset processing
- Exploratory data analysis
- Feature engineering
- Fraud analytics
- AML transaction-monitoring concepts
- Risk-based investigation prioritization
- Analytical validation
- KPI development
- Power BI dashboard design
- DAX calculations
- Data storytelling
- Git and GitHub version control
- Modular Python project development

---

## 🚀 Future Enhancements

Potential extensions to the project include:

- Developing machine-learning models for fraud-risk prediction
- Comparing model-generated risk scores with rule-based indicators
- Adding customer-level behavioral profiling
- Introducing network analysis for connected accounts
- Developing anomaly-detection models
- Creating automated alert-generation workflows
- Adding SQL-based analytical transformations
- Expanding monitoring to additional transaction types
- Implementing model-performance and alert-quality monitoring

These enhancements would extend the project from descriptive and rule-based fraud analytics toward predictive fraud detection.

---

## ⚖️ Disclaimer

This project is an educational and portfolio case study.

The dataset and analytical indicators are used to demonstrate data analytics, fraud analysis, and transaction-monitoring techniques. Risk indicators generated by this project should not be interpreted as proof of money laundering, fraud, or other criminal activity.

In a production environment, alerts would require additional investigation, customer context, regulatory procedures, and appropriate human review.

---

## 👤 Author

**Srinivas Suresh**

Data Analytics | AML & Fraud Analytics | Python | SQL | Power BI

This project was developed as a portfolio case study demonstrating the application of data analytics to financial crime and transaction-monitoring problems.

---

⭐ If you found this project useful, consider starring the repository.
