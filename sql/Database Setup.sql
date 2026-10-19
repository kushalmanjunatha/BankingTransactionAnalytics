-- Set up the database schema before importing the sample CSV.
-- Use MySQL Workbench's Table Data Import Wizard to load:
-- data/processed/PaySim Sample.csv
-- into banking_analytics.banking_transactions.
-- This script creates the table; it does not import the file automatically.

CREATE DATABASE IF NOT EXISTS banking_analytics;
USE banking_analytics;

CREATE TABLE IF NOT EXISTS banking_transactions (
    step INT,
    type VARCHAR(20),
    amount DECIMAL(18, 2),
    nameOrig VARCHAR(30),
    oldbalanceOrg DECIMAL(18, 2),
    newbalanceOrig DECIMAL(18, 2),
    nameDest VARCHAR(30),
    oldbalanceDest DECIMAL(18, 2),
    newbalanceDest DECIMAL(18, 2),
    isFraud TINYINT,
    isFlaggedFraud TINYINT
);

-- After importing, verify the data:
SELECT COUNT(*) AS total_transactions FROM banking_transactions;
