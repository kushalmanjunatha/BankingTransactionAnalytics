
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "PaySim Sample.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Separate training and testing transactions
train_df, test_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["isFraud"]
)

# Prepare features without using fraud labels
def prepare_features(data):
    features = pd.get_dummies(
        data[["type"]],
        dtype=int
    )
    features["log_amount"] = np.log1p(data["amount"])
    features["step"] = data["step"]
    return features

X_train = prepare_features(train_df)
X_test = prepare_features(test_df)

# Ensure train and test have matching columns
X_test = X_test.reindex(
    columns=X_train.columns,
    fill_value=0
)

# Train on training data only
model = IsolationForest(
    n_estimators=200,
    contamination=0.01,
    random_state=42
)

model.fit(X_train)

# Evaluate using unseen test data
test_df = test_df.copy()
test_df["anomaly_score"] = -model.score_samples(X_test)
test_df["is_anomaly"] = (
    model.predict(X_test) == -1
).astype(int)

print("Training records:", len(train_df))
print("Testing records:", len(test_df))
print("Fraud labels in test set:", test_df["isFraud"].sum())
print("Anomalies flagged in test set:", test_df["is_anomaly"].sum())

print("\nTest-set confusion matrix:")
print(pd.crosstab(
    test_df["isFraud"],
    test_df["is_anomaly"]
))

# Rank test transactions by anomaly score
ranked = test_df.sort_values(
    "anomaly_score",
    ascending=False
)

total_fraud = int(test_df["isFraud"].sum())

print("\nTest-set review capacity analysis:")

for n in [50, 100, 200]:
    top_n = ranked.head(n)
    detected = int(top_n["isFraud"].sum())

    precision = detected / n
    recall = detected / total_fraud if total_fraud else 0

    print(
        f"Top {n}: "
        f"Fraud labels found = {detected}, "
        f"Precision = {precision:.2%}, "
        f"Recall = {recall:.2%}"
    )

# Save test results
ranked.to_csv(
    OUTPUT_DIR / "Test Anomaly Results.csv",
    index=False
)

print("\nModel evaluation completed!")


# Investigate where fraud-labelled test records rank

ranked_with_rank = ranked.reset_index(drop=True).copy()

ranked_with_rank["review_rank"] = (
    ranked_with_rank.index + 1
)

fraud_rankings = ranked_with_rank[
    ranked_with_rank["isFraud"] == 1
]

print("\nFraud-labelled transaction rankings:")

print(
    fraud_rankings[
        [
            "review_rank",
            "type",
            "amount",
            "anomaly_score",
            "is_anomaly"
        ]
    ].to_string(index=False)
)

# Count fraud labels at different ranking positions
print("\nFraud labels by ranking group:")

for start, end in [
    (1, 100),
    (101, 200),
    (201, 500),
    (501, 1000)
]:
    count = fraud_rankings[
        fraud_rankings["review_rank"].between(start, end)
    ].shape[0]

    print(f"Ranks {start}-{end}: {count} fraud labels")


# Investigate transaction types in the highest anomaly ranks

print("\nTop 100 anomaly transaction types:")
print(
    ranked.head(100)["type"].value_counts()
)

print("\nRanks 101-200 transaction types:")
print(
    ranked.iloc[100:200]["type"].value_counts()
)

print("\nFraud-labelled transaction types:")
print(
    test_df[test_df["isFraud"] == 1]["type"].value_counts()
)

# Compare amount statistics
print("\nTop 100 transaction amount statistics:")
print(
    ranked.head(100)["amount"].describe()
)

print("\nFraud-labelled transaction amount statistics:")
print(
    test_df[test_df["isFraud"] == 1]["amount"].describe()
)
