from pathlib import Path
import pandas as pd

# Adjusted parents[2] index to properly climb up from src/anomaly/ to root CNAS/
TRANSACTION_FILE = (
    Path(__file__).resolve()
    .parents[2]
    / "data"
    / "processed"
    / "relationships_transactions.csv"
)

# Synced exactly with your CSV column headers
REQUIRED_COLUMNS = [
    "relationship_id",
    "source_id",
    "target_id",
    "amount",
    "timestamp",
]

def load_transactions():
    print("=" * 70)
    print("LOADING TRANSACTION DATA")
    print("=" * 70)
    print(f"File: {TRANSACTION_FILE}")

    if not TRANSACTION_FILE.exists():
        raise FileNotFoundError(
            f"Transaction file not found:\n"
            f"{TRANSACTION_FILE}"
        )

    df = pd.read_csv(TRANSACTION_FILE)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    return df

if __name__ == "__main__":
    df = load_transactions()
    print("\nFirst 5 transactions:")
    print(df.head())
    print("\nMissing values:")
    print(df.isnull().sum())
