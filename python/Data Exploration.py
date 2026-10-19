
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Locate the project folder automatically
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "PaySim Sample.csv"
)

# Load the 50,000-row sample
df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)

print("\nFirst five rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nTransaction types:")
print(df["type"].value_counts())

print("\nFraud-label distribution:")
print(df["isFraud"].value_counts())

print("\nAmount statistics:")
print(df["amount"].describe())


# Create a folder for Python-generated charts
OUTPUT_DIR = PROJECT_DIR / "outputs" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Chart 1: Transaction volume by type
type_counts = df["type"].value_counts()

plt.figure(figsize=(9, 5))
type_counts.plot(kind="bar", color="steelblue")

plt.title("Transaction Volume by Type")
plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "Transaction Volume.png",
    dpi=150
)
plt.close()

# Chart 2: Transaction amount distribution
plt.figure(figsize=(9, 5))

plt.hist(
    df["amount"],
    bins=50,
    color="steelblue",
    edgecolor="white"
)

plt.title("Transaction Amount Distribution")
plt.xlabel("Transaction Amount")
plt.ylabel("Number of Transactions")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "Amount Distribution.png",
    dpi=150
)
plt.close()

print("\nCharts saved successfully!")
