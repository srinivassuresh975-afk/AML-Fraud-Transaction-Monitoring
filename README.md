# 🛡️ AML Fraud Analytics & Transaction Monitoring

> An end-to-end Data Analytics case study transforming large-scale financial transaction data into actionable AML and fraud intelligence using **Python, SQL concepts, feature engineering, exploratory data analysis, and Power BI**.

The project simulates a real-world transaction-monitoring workflow: processing raw transaction data, engineering fraud-risk indicators, validating suspicious behavior, and presenting management-level insights through an interactive Power BI dashboard.

---

## 📊 Dashboard Preview

### Executive Fraud Intelligence Dashboard

![AML Fraud Intelligence Dashboard](screenshots/executive_overview.png)

### Transaction Investigation Dashboard

![AML Case Investigation Dashboard](screenshots/investigation_detail.png)

---

## 🎯 Executive Summary

The objective of this project was to build an analytics-driven transaction monitoring framework capable of identifying fraudulent activity, suspicious transaction behavior, high-risk transactions, and investigation priorities from a large financial transaction dataset.

The final analytical dataset contains approximately **2.77 million transactions** focused on **CASH_OUT** and **TRANSFER** activity.

Key portfolio findings include:

- **2.77M** analyzed transactions
- **8.21K** confirmed fraudulent transactions
- Approximately **0.30%** overall fraud rate
- Approximately **12.06bn** in confirmed fraud exposure
- Approximately **1.20M** large-value transactions
- Approximately **8.02K** structuring alerts
- Fraud activity concentrated within **CASH_OUT** and **TRANSFER** transactions

The project demonstrates how data analytics can support fraud investigation teams by converting transaction-level data into prioritized risk intelligence.

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

The project follows a structured analytics pipeline:

```text
Raw Transaction Data
        │
        ▼
┌─────────────────────┐
│   Data Extraction   │
│      extract.py     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Data Transformation │
│    transform.py     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────┐
│   Feature Engineering   │
│ feature_engineering.py  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────┐
│ Data Validation     │
│   validation.py     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Exploratory Analysis│
│       eda.py        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Power BI Model    │
└──────────┬──────────┘
           │
           ▼
Executive Dashboard + Investigation Queue