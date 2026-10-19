
USE banking_analytics;

-- 1. Compare transaction volume and fraud-label rates by type
WITH transaction_summary AS (
    SELECT
        type,
        COUNT(*) AS total_transactions,
        SUM(isFraud) AS fraud_label_count,
        SUM(amount) AS total_amount,
        AVG(amount) AS average_amount
    FROM banking_transactions
    GROUP BY type
)
SELECT
    type,
    total_transactions,
    fraud_label_count,
    ROUND(
        100.0 * fraud_label_count / total_transactions, 3
    ) AS fraud_label_rate_pct,
    ROUND(total_amount, 2) AS total_amount,
    ROUND(average_amount, 2) AS average_amount
FROM transaction_summary
ORDER BY fraud_label_rate_pct DESC;


-- 2. Rank fraud-labelled transactions by amount
WITH ranked_transactions AS (
    SELECT
        type,
        amount,
        nameOrig,
        nameDest,
        ROW_NUMBER() OVER (
            ORDER BY amount DESC
        ) AS transaction_rank
    FROM banking_transactions
    WHERE isFraud = 1
)
SELECT
    transaction_rank,
    type,
    amount,
    nameOrig,
    nameDest
FROM ranked_transactions
WHERE transaction_rank <= 10
ORDER BY transaction_rank;


-- 3. Compare each transaction with its type's average
WITH type_averages AS (
    SELECT
        type,
        AVG(amount) AS average_type_amount
    FROM banking_transactions
    GROUP BY type
)
SELECT
    b.type,
    COUNT(*) AS transaction_count,
    ROUND(AVG(b.amount), 2) AS average_amount,
    ROUND(MAX(t.average_type_amount), 2) AS type_average,
    SUM(b.isFraud) AS fraud_label_count
FROM banking_transactions AS b
JOIN type_averages AS t
    ON b.type = t.type
GROUP BY b.type
ORDER BY average_amount DESC;


-- 4. Compare amounts for fraud-labelled and
-- non-fraud-labelled transactions by type

SELECT
    type,
    SUM(CASE WHEN isFraud = 1 THEN 1 ELSE 0 END)
        AS fraud_label_count,

    ROUND(
        AVG(CASE WHEN isFraud = 1 THEN amount END), 2
    ) AS avg_fraud_label_amount,

    ROUND(
        AVG(CASE WHEN isFraud = 0 THEN amount END), 2
    ) AS avg_non_fraud_label_amount,

    ROUND(
        MAX(CASE WHEN isFraud = 1 THEN amount END), 2
    ) AS largest_fraud_label_amount

FROM banking_transactions
GROUP BY type
ORDER BY fraud_label_count DESC;
