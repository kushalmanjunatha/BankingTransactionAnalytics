
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "PaySim Sample.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_FILE)

# Features used to detect unusual transactions
X = pd.get_dummies(df[["type"]], dtype=int)
X["log_amount"] = np.log1p(df["amount"])
X["step"] = df["step"]

# Build the anomaly detection model
model = IsolationForest(
    n_estimators=200,
    contamination=0.01,
    random_state=42
)

# -1 means anomaly, 1 means normal
predictions = model.fit_predict(X)

df["is_anomaly"] = (predictions == -1).astype(int)

# Summary
print("Total transactions:", len(df))
print("Flagged anomalies:", df["is_anomaly"].sum())
print("Fraud-labelled transactions:", df["isFraud"].sum())

# Compare anomaly flags with known synthetic labels
print("\nFraud labels vs anomaly flags:")
print(pd.crosstab(
    df["isFraud"],
    df["is_anomaly"],
    rownames=["Fraud Label"],
    colnames=["Anomaly Flag"]
))

# Calculate basic evaluation metrics
true_positive = (
    (df["isFraud"] == 1) &
    (df["is_anomaly"] == 1)
).sum()

flagged = df["is_anomaly"].sum()
actual_fraud_labels = df["isFraud"].sum()

precision = true_positive / flagged if flagged else 0
recall = true_positive / actual_fraud_labels if actual_fraud_labels else 0

print(f"\nPrecision: {precision:.2%}")
print(f"Recall: {recall:.2%}")

# Save transactions flagged by the model
anomalies = df[df["is_anomaly"] == 1].copy()
anomalies.to_csv(
    OUTPUT_DIR / "Flagged Transactions.csv",
    index=False
)

print("\nAnomaly analysis completed!")
print("Results saved to:", OUTPUT_DIR)



# Rank transactions by anomaly score
# Higher score means more unusual
df["anomaly_score"] = -model.score_samples(X)

ranked_df = df.sort_values(
    by="anomaly_score",
    ascending=False
)

print("\nModel evaluation by review capacity:")
print("-" * 65)

for top_n in [100, 250, 500, 1000]:

    top_transactions = ranked_df.head(top_n)

    detected = int(
        top_transactions["isFraud"].sum()
    )

    precision = detected / top_n

    recall = detected / int(df["isFraud"].sum())

    print(
        f"Top {top_n:4d} | "
        f"Fraud labels found: {detected:3d} | "
        f"Precision: {precision:.2%} | "
        f"Recall: {recall:.2%}"
    )

# Save ranked transactions for further analysis
ranked_df.to_csv(
    OUTPUT_DIR / "Ranked Anomaly Transactions.csv",
    index=False
)

print("\nRanked anomaly analysis saved!")
