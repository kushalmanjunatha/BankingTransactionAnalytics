# Banking Transaction Risk Analytics

**End-to-end data analytics portfolio | Excel • MySQL • Power BI • Python • Isolation Forest**

> **Dataset and scope:** This is an educational analysis of the **first 50,000 rows** of the **synthetic PaySim transaction dataset**, not transactions from an Australian bank. Fraud labels and transaction amounts are simulated. Results should not be interpreted as actual bank losses or production fraud-detection performance.

## Overview

The analysis uses the [PaySim synthetic financial transactions dataset](https://www.kaggle.com/datasets/ealaxi/paysim1), published by Edgar Lopez-Rojas. The source dataset page lists a **CC BY-SA 4.0** licence. The dataset is not redistributed in this repository.

This project explores transaction patterns and fraud-labelled activity, builds an interactive Power BI report, and assesses whether unsupervised anomaly scoring can help prioritise transactions for investigation. It emphasises honest validation and business interpretation rather than overstating model accuracy.

## Project highlights

- Analysed **50,000 synthetic transactions** and identified **100 fraud-labelled records (0.20%)** in the sample.
- Built a **two-page interactive Power BI dashboard** for transaction monitoring and risk exploration.
- Compared **two Isolation Forest feature sets** across **five validation splits**, using precision, recall and a fixed review capacity.
- Documented findings, false-positive trade-offs and limitations to support careful interpretation.

**Questions explored**

- How does transaction activity differ between PAYMENT, CASH_OUT, CASH_IN, TRANSFER and DEBIT?
- Which transaction categories have higher observed fraud-label rates?
- How does transaction amount relate to fraud-labelled activity?
- Can Isolation Forest prioritise unusual transactions at limited investigation capacity?
- Are model results stable across repeated validation samples?

## Dashboard

The included Power BI report has **two pages**:

1. **Executive Overview** — KPIs, transaction activity, fraud-label analysis and key findings.
2. **Risk Investigation** — comparisons, investigation-focused findings and experimental anomaly-model results.

**Open in Power BI Desktop:** [`powerbi/Banking Risk Dashboard.pbix`](powerbi/Banking%20Risk%20Dashboard.pbix)

> The Power BI report and screenshots of both dashboard pages are included. The PBIX contains a saved model; refreshing it on another computer may require updating the MySQL or local file source.

![Executive Overview](powerbi/screenshots/Executive%20Overview.png)

![Risk Investigation](powerbi/screenshots/Risk%20Investigation.png)

**Project reports:** [Business risk insights](reports/Banking%20Risk%20Insights.md) · [Executive summary](reports/Executive%20Summary.md)  
**Excel analysis:** [Transaction analysis workbook](excel/Banking%20Transaction%20Analysis.xlsx)

## Tools and techniques

| Stage | Tools and demonstrated skills |
|---|---|
| Excel | PivotTables, transaction summaries, KPI analysis |
| SQL | MySQL, aggregates, CASE, CTEs, JOINs and window functions |
| Power BI | DAX measures, KPI cards, comparisons, report pages and slicers |
| Python EDA | Pandas, NumPy, Matplotlib, distributions and data-quality checks |
| Machine learning | scikit-learn Isolation Forest, anomaly ranking, precision/recall and validation |
| Reporting and communication | Evidence-based insights, technical limitations and business recommendations |

## Selected business findings

The 50,000-row sample contains **100 fraud-labelled transactions (0.20%)**.

| Type | Transactions | Fraud-labelled | Label rate |
|---|---:|---:|---:|
| TRANSFER | 4,700 | 49 | 1.043% |
| CASH_OUT | 13,756 | 51 | 0.371% |
| CASH_IN | 8,992 | 0 | 0.000% |
| DEBIT | 640 | 0 | 0.000% |
| PAYMENT | 21,912 | 0 | 0.000% |

The mean amount of fraud-labelled CASH_OUT transactions was higher than the mean of other CASH_OUT transactions, whereas the pattern was reversed for TRANSFER. **Amount alone is not a consistent identifier of fraud-labelled activity.**

### Exploratory Python charts

![Transaction volume by type](outputs/charts/Transaction%20Volume.png)

![Transaction amount distribution](outputs/charts/Amount%20Distribution.png)

## Anomaly-detection evaluation

Two Isolation Forest feature sets were compared:

- **Model A:** transaction type, log-transformed amount and transaction step.
- **Model B:** log-transformed amount and transaction step.

Five repeated stratified validation splits were evaluated using a **top-2% review capacity** (160 of 8,000 validation records in each split).

| Mean validation result | Model A | Model B |
|---|---:|---:|
| Fraud labels found per split | 2.6 | 1.6 |
| Precision at top 2% | 1.625% | 1.000% |
| Recall at top 2% | 16.25% | 10.00% |

Model B performed better on one split, but Model A performed better on average across five splits. Performance varied substantially and **neither model reliably identified fraud-labelled transactions**. Isolation Forest detects statistical unusualness, not fraud directly.

**Evaluation caveats:** Fraud-labelled cases are rare; repeated validation sets overlap; the initial test set was examined during development and is no longer an unbiased final test. The sample is the earliest 50,000 PaySim rows rather than a random or fully representative sample. A fresh held-out period with time-aware evaluation would be required to support stronger generalisation claims.

## Business recommendations

1. Treat anomaly scores as **investigation support**, never automatic proof of fraud.
2. Examine TRANSFER and CASH_OUT behaviour further while acknowledging that these findings relate only to the synthetic sample.
3. Compare the cost of missed labels and manual review volumes across thresholds.
4. Validate on genuinely unseen and preferably later-time data before considering practical use.

## Business value

This portfolio analysis demonstrates how transaction data can support risk-monitoring and investigation workflows:

- **Transaction monitoring:** Used Power BI to examine transaction volumes, amounts and fraud-labelled activity.
- **Risk analysis:** Compared observed fraud-label rates and amount patterns across transaction types.
- **Investigation prioritisation:** Evaluated anomaly-ranking methods under a limited manual-review capacity.
- **Decision support:** Communicated findings alongside model uncertainty and practical validation requirements.

## Project files

```text
Banking Transaction Analytics/
├── README.md
├── .gitignore
├── requirements.txt
├── excel/
│   └── Banking Transaction Analysis.xlsx
├── data/
│   ├── README.md
│   └── raw/
│       └── Create PaySim Sample.py
├── sql/
│   ├── Database Setup.sql
│   ├── Transaction Overview.sql
│   ├── Fraud Analysis.sql
│   ├── Amount Risk Analysis.sql
│   ├── Fraud Rate by Amount.sql
│   └── Advanced Risk Analysis.sql
├── python/
│   ├── Data Exploration.py
│   ├── Anomaly Detection.py
│   ├── Model Evaluation.py
│   ├── Compare Models.py
│   └── Model Stability.py
├── powerbi/
│   ├── Banking Risk Dashboard.pbix
│   └── screenshots/
│       ├── Executive Overview.png
│       └── Risk Investigation.png
├── outputs/
│   └── charts/
│       ├── Transaction Volume.png
│       └── Amount Distribution.png
└── reports/
    ├── Banking Risk Insights.md
    └── Executive Summary.md
```

**Raw CSVs, the processed sample CSV, and transaction-level model exports are intentionally excluded from this GitHub-ready ZIP.** The Excel workbook and Power BI report retain saved analysis/results; an Excel external CSV link or Power BI data-source connection may need updating to refresh on a different computer.

## How to reproduce

1. Download the original CSV from the [PaySim dataset page on Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1) and follow its licence and usage terms. This repository does not redistribute the source or processed dataset.
2. Place the original PaySim CSV in `data/raw/` (for example, name it `PaySim Original.csv`). The sample-generation script reads the first `.csv` it finds in that folder.
3. Install dependencies from the project root:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Create the exact first-50,000-row sample used here:

   ```powershell
   python "data/raw/Create PaySim Sample.py"
   ```

   This writes `data/processed/PaySim Sample.csv`. The published results assume the original source CSV and its row order; using a differently sorted dataset may produce different results.

5. Run the Python scripts from the project root:

   ```powershell
   python "python/Data Exploration.py"
   python "python/Anomaly Detection.py"
   python "python/Model Evaluation.py"
   python "python/Compare Models.py"
   python "python/Model Stability.py"
   ```

6. To reproduce the SQL work, run `sql/Database Setup.sql` in MySQL Workbench, import `data/processed/PaySim Sample.csv` into `banking_analytics.banking_transactions`, and execute the remaining five SQL files in order (`sql/Transaction Overview.sql` through `sql/Advanced Risk Analysis.sql`).
7. Open the `.pbix` file in Power BI Desktop. Update the local MySQL connection or credentials if a refresh is necessary.

## Project Limitations

This project uses synthetic banking transaction data and exploratory anomaly detection using Isolation Forest. Model performance was evaluated on sampled data and should not be interpreted as real-world fraud detection performance. The analysis is intended for learning, portfolio demonstration and identifying potential transaction-risk patterns.
