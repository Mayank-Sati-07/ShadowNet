from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_accounts.csv"
)

accounts = pd.DataFrame({
    "account_id": df["account_id"],
    "account_type": df["account_type"],
    "source": df["data_provenance"]
})

accounts = accounts.drop_duplicates(
    subset=["account_id"]
)

accounts.to_csv(
    OUT_DIR / "accounts.csv",
    index=False
)