from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_phones.csv"
)

phones = pd.DataFrame({
    "phone_id": df["phone_id"],
    "phone_type": df["phone_type"],
    "source": df["data_provenance"]
})

phones = phones.drop_duplicates(
    subset=["phone_id"]
)

phones.to_csv(
    OUT_DIR / "phones.csv",
    index=False
)

print(f"Phones created: {len(phones)}")