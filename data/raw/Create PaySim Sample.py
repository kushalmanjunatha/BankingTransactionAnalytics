
import pandas as pd
from pathlib import Path

# Locate the folder containing this Python script
script_folder = Path(__file__).resolve().parent

# Your script is currently inside data/raw
raw_folder = script_folder

# Find CSV files, excluding this script (which is not a CSV anyway)
csv_files = list(raw_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV file found in this folder: {raw_folder}\n"
        "Check that the PaySim CSV has been extracted here."
    )

file_path = csv_files[0]
print(f"Reading file: {file_path}")

# Read 50,000 rows for Excel practice
df = pd.read_csv(file_path, nrows=50000)

# Create the processed folder in the main project directory
project_folder = script_folder.parent.parent
output_folder = project_folder / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

output_path = output_folder / "PaySim Sample.csv"
df.to_csv(output_path, index=False)

print("\nSample created successfully!")
print("Rows and columns:", df.shape)
print("Saved to:", output_path)
