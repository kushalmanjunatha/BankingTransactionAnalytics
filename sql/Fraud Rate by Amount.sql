
USE banking_analytics;

SELECT
    CASE
        WHEN amount < 1000 THEN 'Under 1,000'
        WHEN amount < 10000 THEN '1,000-9,999'
        WHEN amount < 100000 THEN '10,000-99,999'
        WHEN amount < 1000000 THEN '100,000-999,999'
        ELSE '1,000,000 and above'
    END AS amount_range,

    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_label_count,

    ROUND(
        100.0 * SUM(isFraud) / COUNT(*),
        3
    ) AS fraud_label_rate_pct

FROM banking_transactions
GROUP BY amount_range
ORDER BY
    CASE amount_range
        WHEN 'Under 1,000' THEN 1
        WHEN '1,000-9,999' THEN 2
        WHEN '10,000-99,999' THEN 3
        WHEN '100,000-999,999' THEN 4
        ELSE 5
    END;
