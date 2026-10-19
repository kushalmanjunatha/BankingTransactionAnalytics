
USE banking_analytics;

-- Compare transaction amounts for each fraud label
SELECT
    isFraud,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount), 2) AS average_amount,
    ROUND(
        AVG(amount * amount),
        2
    ) AS average_squared_amount,
    ROUND(MIN(amount), 2) AS minimum_amount,
    ROUND(MAX(amount), 2) AS maximum_amount
FROM banking_transactions
GROUP BY isFraud;

-- Compare amount ranges by fraud label
SELECT
    CASE
        WHEN amount < 1000 THEN 'Under 1,000'
        WHEN amount < 10000 THEN '1,000-9,999'
        WHEN amount < 100000 THEN '10,000-99,999'
        WHEN amount < 1000000 THEN '100,000-999,999'
        ELSE '1,000,000 and above'
    END AS amount_range,
    isFraud,
    COUNT(*) AS transaction_count
FROM banking_transactions
GROUP BY amount_range, isFraud
ORDER BY amount_range, isFraud;
