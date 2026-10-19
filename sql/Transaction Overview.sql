
USE banking_analytics;

-- 1. Check the total number of transactions
SELECT COUNT(*) AS total_transactions
FROM banking_transactions;

-- 2. Summarise transactions by type
SELECT
    type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount
FROM banking_transactions
GROUP BY type
ORDER BY transaction_count DESC;

-- 3. Identify the largest transactions
SELECT
    type,
    amount,
    nameOrig,
    nameDest
FROM banking_transactions
ORDER BY amount DESC
LIMIT 10;

-- 4. Compare transactions labelled as fraud
SELECT
    isFraud,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM banking_transactions
GROUP BY isFraud;

-- 5. Compare fraud labels by transaction type
SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_label_count,
    ROUND(100.0 * SUM(isFraud) / COUNT(*), 2) AS fraud_label_percentage
FROM banking_transactions
GROUP BY type
ORDER BY fraud_label_count DESC;
