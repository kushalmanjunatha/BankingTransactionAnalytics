# Banking Transaction Risk — Executive Summary

**Dataset:** PaySim synthetic financial transactions  
**Sample:** 50,000 transactions  
**Tools:** Excel, MySQL, Power BI, Python and Isolation Forest

## Executive Summary

This project examines whether transaction analysis and anomaly detection can help prioritise potentially suspicious records for manual review.

An analysis of 50,000 synthetic financial transactions identified 100 fraud-labelled records, representing 0.20% of the dataset.

TRANSFER transactions recorded the highest fraud-label rate at 1.043%, followed by CASH_OUT at 0.371%. No fraud-labelled records were observed in the remaining three transaction categories within the sample.

Transaction amount analysis showed that fraud-labelled CASH_OUT transactions had a higher average amount than non-fraud-labelled CASH_OUT transactions. However, the opposite pattern was observed for TRANSFER transactions, indicating that transaction amount alone is not a reliable indicator of fraud-labelled activity.

## Anomaly Detection Findings

Two Isolation Forest models were evaluated to investigate whether unusual transaction patterns could help prioritise records for review.

Across five validation splits, Model A, using transaction type, log-transformed amount and transaction step, achieved an average recall of 16.25% at a 2% review capacity. Model B, using only log-transformed amount and step, achieved an average recall of 10%.

Model performance varied between validation samples. The findings suggest that anomaly detection may help identify transactions requiring investigation, but the models are not sufficiently reliable for automated fraud decisions.

## Business Recommendations

1. Prioritise further investigation of TRANSFER and CASH_OUT transaction patterns, while recognising that the results are specific to this synthetic sample.
2. Use anomaly scores as supporting information for human review rather than automatically classifying transactions as fraudulent.
3. Compare different review capacities and investigate false positives to assess operational usefulness.
4. Test additional features and more realistic validation approaches before considering practical deployment.

## Limitations

The analysis uses synthetic PaySim data rather than real Australian banking transactions. The sample has a highly imbalanced fraud-label distribution, and model performance is inconsistent across validation splits. The original test sample has already been inspected, so the results should be treated as exploratory rather than an unbiased final performance estimate.
