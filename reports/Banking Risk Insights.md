# Banking Transaction Risk Analytics — Business Insights Report

## 1. Project objective

Analyse transaction activity, identify unusual patterns and assess whether anomaly detection can help prioritise transactions for manual investigation.

**Dataset:** PaySim synthetic financial transactions (first 50,000 rows)  
**Sample size:** 50,000 transactions

## 2. Key transaction findings

- **Total transactions:** 50,000.
- **Fraud-labelled transactions:** 100 (0.20%).
- **TRANSFER fraud-label rate:** 1.043%.
- **CASH_OUT fraud-label rate:** 0.371%.
- No fraud-labelled records were observed in CASH_IN, PAYMENT or DEBIT **within this sample**.

## 3. Transaction amount insights

The mean transaction amounts differ between fraud-labelled and non-fraud-labelled records within each category:

| Transaction type | Fraud-labelled mean amount | Non-fraud-labelled mean amount |
|---|---:|---:|
| CASH_OUT | 559,277.75 | 181,938.02 |
| TRANSFER | 589,196.06 | 759,880.42 |

Fraud-labelled CASH_OUT transactions had a higher average amount than their non-fraud-labelled counterparts, while the opposite pattern was observed for TRANSFER. **Transaction amount alone does not consistently distinguish fraud-labelled activity.** These values come from synthetic data and should not be interpreted as actual bank losses.

## 4. Anomaly detection evaluation

**Algorithm:** Isolation Forest (scikit-learn)

- **Model A:** transaction type, log-transformed amount and transaction step.
- **Model B:** log-transformed amount and transaction step.

The models were compared across **five repeated validation splits** at a **2% review capacity** (the top 160 ranked records in each 8,000-row validation split).

| Average validation metric | Model A | Model B |
|---|---:|---:|
| Fraud labels found per split | 2.6 | 1.6 |
| Precision at top 2% | 1.625% | 1.000% |
| Recall at top 2% | 16.25% | 10.00% |

Model A performed better **on average** across the five splits, but performance varied, and neither model consistently identified fraud-labelled transactions. The scores indicate unusualness, **not proof of fraud**. The fixed review capacity means most records would not be manually investigated.

## 5. Business recommendations

1. Use anomaly scores only to **prioritise manual investigation**, not to automatically label transactions as fraudulent.
2. Examine TRANSFER and CASH_OUT patterns further, since these contain all fraud-labelled records **in this sample**.
3. Review false-positive volumes and the costs of missed fraud labels when selecting review-capacity thresholds.
4. Test additional features, improved validation methods and more realistic review scenarios before considering deployment.

## 6. Limitations

- PaySim contains **synthetic**, not real banking transactions; conclusions are not evidence of real-world fraud-detection performance.
- The analysis uses the **first 50,000 rows** of the source dataset, which may not be representative.
- Fraud labels are rare and validation results vary across repeated splits, which overlap.
- The initial test set has already been inspected and is not an unbiased final evaluation.
- The models are **exploratory and not production-ready**; time-aware evaluation on unseen data would be needed for stronger claims.
