# AML Fraud Analytics & Transaction Monitoring Dashboard

An end-to-end Data Analytics project that analyzes large-scale financial transaction data to identify fraud patterns, AML risk indicators, suspicious transaction behavior, and investigation priorities.

The project combines **Python-based data processing, feature engineering, exploratory data analysis, and Power BI visualization** to simulate a real-world AML / Fraud Transaction Monitoring workflow.

## 📊 Dashboard Preview

### Executive Overview

![AML Fraud Intelligence Dashboard](screenshots/executive_overview.png)

### Investigation Detail

![AML Case Investigation Dashboard](screenshots/investigation_detail.png)

---

## 🎯 Project Objective

The objective of this project is to transform raw financial transaction data into actionable fraud and AML intelligence.

The analysis focuses on:

- Detecting confirmed fraudulent transactions
- Identifying high-risk and large-value transactions
- Detecting potential structuring behavior
- Assigning transaction risk scores and risk levels
- Analyzing fraud by transaction type and time of day
- Identifying origin accounts with significant fraud exposure
- Creating an investigation queue for transaction review
- Presenting management-level KPIs through an interactive Power BI dashboard

---

## 🔍 Key Insights

Analysis of approximately **2.77 million transactions** identified:

- **8.21K confirmed fraudulent transactions**
- Overall fraud rate of approximately **0.30%**
- Approximately **12.06bn in fraud exposure**
- **CASH_OUT** and **TRANSFER** as the transaction types associated with confirmed fraud in the analyzed data
- Approximately **1.20M large transactions**
- Approximately **8.02K structuring alerts**

The dashboard also provides transaction-level investigation capabilities using risk scores, risk levels, fraud status, account information, transaction amount, and behavioral red flags.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analytics |
| Pandas | Data cleaning, transformation and aggregation |
| NumPy | Numerical operations |
| Power BI | Interactive dashboard and investigation reporting |
| DAX | KPI measures and analytical calculations |
| Git / GitHub | Version control and project portfolio |
| VS Code | Development environment |

---

## ⚙️ Analytics Pipeline

The project follows a structured analytics workflow:

```text
Raw Transaction Data
        ↓
Data Extraction
        ↓
Data Cleaning & Transformation
        ↓
Validation
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis
        ↓
Summary / Reporting Tables
        ↓
Power BI Dashboard
        ↓
Fraud & AML Investigation Insights
```

---

## 🚩 Risk & Fraud Indicators

The analytical layer includes indicators designed to support transaction monitoring, including:

- Confirmed fraud status
- Large transaction detection
- Structuring indicators
- Round-amount indicators
- High-value transaction indicators
- Origin and destination balance behavior
- Transaction risk scoring
- Risk classification
- Transaction timing patterns

These indicators are combined to support prioritization of potentially suspicious transactions for further investigation.

---

## 📈 Power BI Dashboard

The Power BI report contains two analytical views.

### 1. Executive Overview

Provides management-level visibility into:

- Total transactions
- Fraud amount
- Fraud transactions
- Fraud percentage
- Large transactions
- Structuring alerts
- Fraud by transaction type
- Fraud vs legitimate transactions
- Transaction risk distribution
- Fraud activity by hour of day
- Recommended investigation actions

### 2. Investigation Detail

Designed for transaction-level review with:

- Transaction investigation queue
- Origin and destination accounts
- Transaction amount
- Risk score
- Risk level
- Fraud status
- Red-flag indicators
- Top origin accounts by fraud amount
- Interactive transaction, risk, fraud-status, and day filters

---

## 📁 Project Structure

```text
AML-Fraud-Analytics/
│
├── dashboard/
│   └── Visualization.pbix
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── enriched/
│   └── reports/
│       ├── aml_summary.csv
│       ├── red_flag_summary.csv
│       ├── risk_level_summary.csv
│       └── transaction_type_summary.csv
│
├── docs/
├── logs/
├── notebooks/
├── screenshots/
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

---

## 🔄 ETL & Analysis Components

### Extract
Loads the source financial transaction dataset for downstream processing.

### Transform
Cleans and prepares transaction data for analysis.

### Validation
Performs data-quality checks to improve reliability before analytical processing.

### Feature Engineering
Creates analytical fraud and AML indicators used for transaction risk assessment.

### Exploratory Data Analysis
Analyzes transaction behavior, fraud patterns, risk distribution, and red-flag characteristics.

### Power BI
Transforms analytical outputs into interactive executive and investigation dashboards.

---

## 📂 Dataset

The project uses a large synthetic financial transaction dataset containing transaction types, account balances, transaction amounts, and labelled fraudulent activity.

The original raw dataset is intentionally **not stored in this GitHub repository** because of its large file size.

This repository instead focuses on the analytics pipeline, project methodology, reporting outputs, dashboard, and documentation.

---

## 💼 Business Value

This project demonstrates how transaction data can be transformed into an AML/Fraud monitoring solution that helps analysts:

- Prioritize high-risk transactions
- Detect suspicious behavioral patterns
- Investigate potentially fraudulent accounts
- Reduce manual review effort through risk-based prioritization
- Communicate fraud exposure through management dashboards
- Support data-driven AML and fraud investigation decisions

---

## 👤 Author

**Srinivas Suresh**

Data Analytics | SQL | Python | Power BI | AML & Fraud Analytics