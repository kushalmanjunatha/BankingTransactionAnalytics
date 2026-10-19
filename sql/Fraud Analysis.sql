
USE banking_analytics;

-- 1. Compare average transaction amounts
-- for fraud-labelled and non-fraud-labelled records
SELECT
    isFraud,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount), 2) AS average_amount,
    ROUND(MAX(amount), 2) AS maximum_amount,
    ROUND(SUM(amount), 2) AS total_amount
FROM banking_transactions
GROUP BY isFraud;

-- 2. Analyse fraud labels by transaction type
SELECT
    type,
    SUM(isFraud) AS fraud_count,
    ROUND(SUM(amount * isFraud), 2) AS fraud_label_amount,
    ROUND(
        100.0 * SUM(isFraud) / COUNT(*), 2
    ) AS fraud_label_rate_pct
FROM banking_transactions
GROUP BY type
ORDER BY fraud_count DESC;

-- 3. Check for transactions with unusually large amounts
SELECT
    type,
    COUNT(*) AS large_transaction_count,
    ROUND(AVG(amount), 2) AS average_amount
FROM banking_transactions
WHERE amount >= 1000000
GROUP BY type
ORDER BY large_transaction_count DESC;
