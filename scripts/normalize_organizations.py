from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_organizations.csv"
)

organizations = pd.DataFrame({
    "organization_id": df["organization_id"],
    "organization_type": df["organization_type"],
    "source": df["data_provenance"]
})

organizations = organizations.drop_duplicates(
    subset=["organization_id"]
)

organizations.to_csv(
    OUT_DIR / "organizations.csv",
    index=False
)

print(
    f"Organizations created: {len(organizations)}"
)