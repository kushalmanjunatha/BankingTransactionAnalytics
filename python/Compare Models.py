
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest

# Load the dataset
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "PaySim Sample.csv"

df = pd.read_csv(DATA_FILE)

# Reproduce our previous 80/20 split.
# Keep the previously examined test data out
# of this model comparison.
development_df, _ = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["isFraud"]
)

# Split development data into training and validation
train_df, val_df = train_test_split(
    development_df,
    test_size=0.20,
    random_state=42,
    stratify=development_df["isFraud"]
)

print("Training transactions:", len(train_df))
print("Validation transactions:", len(val_df))
print("Fraud labels in validation:", int(val_df["isFraud"].sum()))


def prepare_features(data, include_type=True):
    # Log-transform amounts because values are skewed
    features = pd.DataFrame(index=data.index)
    features["log_amount"] = np.log1p(data["amount"])
    features["step"] = data["step"]

    if include_type:
        types = pd.get_dummies(
            data["type"],
            prefix="type",
            dtype=int
        )
        features = pd.concat([features, types], axis=1)

    return features


def evaluate_model(name, include_type):
    X_train = prepare_features(train_df, include_type)
    X_val = prepare_features(val_df, include_type)

    X_val = X_val.reindex(
        columns=X_train.columns,
        fill_value=0
    )

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42
    )

    model.fit(X_train)

    results = val_df.copy()
    results["anomaly_score"] = -model.score_samples(X_val)

    ranked = results.sort_values(
        "anomaly_score",
        ascending=False
    )

    # Review the most unusual 2% of validation rows
    review_limit = int(len(ranked) * 0.02)
    reviewed = ranked.head(review_limit)

    found = int(reviewed["isFraud"].sum())
    total_fraud = int(val_df["isFraud"].sum())

    precision = found / review_limit
    recall = found / total_fraud if total_fraud else 0

    print(f"\n{name}")
    print("-" * 40)
    print("Transactions reviewed:", review_limit)
    print("Fraud labels found:", found)
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")

    print("\nTop 100 transaction types:")
    print(ranked.head(100)["type"].value_counts())

    return {
        "model": name,
        "fraud_found": found,
        "precision": precision,
        "recall": recall
    }


model_a = evaluate_model(
    "Model A - Original",
    include_type=True
)

model_b = evaluate_model(
    "Model B - Simplified",
    include_type=False
)

print("\nMODEL COMPARISON")
print("=" * 45)

comparison = pd.DataFrame([model_a, model_b])
print(comparison.to_string(index=False))
