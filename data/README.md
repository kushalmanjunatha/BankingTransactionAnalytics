# Dataset setup

The raw PaySim CSV and its 50,000-row derived sample are intentionally not included in this public GitHub package. Obtain the source from its distributor and check the applicable terms before use.

1. Download the original PaySim synthetic financial transaction CSV from its original public distribution source, observing the relevant licensing and usage terms.
2. Place the original PaySim CSV in `data/raw/` (you may rename it `PaySim Original.csv`).
3. From the repository root run:

   ```powershell
   python "data/raw/Create PaySim Sample.py"
   ```

The script selects the **first 50,000 rows** in the CSV and writes `data/processed/PaySim Sample.csv`. It does **not** randomly sample rows; the resulting figures are specific to this early segment of the PaySim simulation.
