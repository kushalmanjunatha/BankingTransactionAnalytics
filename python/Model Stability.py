
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    StratifiedShuffleSplit
)
from sklearn.ensemble import IsolationForest

PROJECT_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    PROJECT_DIR / "data" / "processed" / "PaySim Sample.csv"
)

# Keep previously examined test data out
development_df, _ = train_test_split(
    df,
    test_size=0.20,
    stratify=df["isFraud"],
    random_state=42
)

def make_features(data, include_type):
    X = pd.DataFrame(index=data.index)

    X["log_amount"] = np.log1p(data["amount"])
    X["step"] = data["step"]

    if include_type:
        dummies = pd.get_dummies(
            data["type"],
            dtype=int
        )
        X = pd.concat([X, dummies], axis=1)

    return X

splitter = StratifiedShuffleSplit(
    n_splits=5,
    test_size=0.20,
    random_state=42
)

results = []

for split_number, (train_idx, val_idx) in enumerate(
    splitter.split(
        development_df,
        development_df["isFraud"]
    ),
    start=1
):
    train = development_df.iloc[train_idx]
    val = development_df.iloc[val_idx]

    for name, include_type in [
        ("Model A", True),
        ("Model B", False)
    ]:
        X_train = make_features(train, include_type)
        X_val = make_features(val, include_type)

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

        # Higher score = more unusual
        scores = -model.score_samples(X_val)

        ranked = val.copy()
        ranked["score"] = scores

        review_limit = int(len(val) * 0.02)

        top = ranked.nlargest(
            review_limit,
            "score"
        )

        found = int(top["isFraud"].sum())
        total_fraud = int(val["isFraud"].sum())

        results.append({
            "split": split_number,
            "model": name,
            "found": found,
            "precision": found / review_limit,
            "recall": found / total_fraud
        })

results_df = pd.DataFrame(results)

print("\nRESULTS BY VALIDATION SPLIT")
print(results_df.to_string(index=False))

print("\nAVERAGE MODEL PERFORMANCE")
print(
    results_df.groupby("model")[
        ["found", "precision", "recall"]
    ].agg(["mean", "std"]).round(4)
)

print("\nStability analysis completed!")
