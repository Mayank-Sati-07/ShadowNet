from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_locations.csv"
)

locations = pd.DataFrame({
    "location_id": df["location_id"],
    "city": df["city"],
    "location_type": df["location_type"],
    "source": df["data_provenance"]
})

locations = locations.drop_duplicates(
    subset=["location_id"]
)

locations.to_csv(
    OUT_DIR / "locations.csv",
    index=False
)

print(f"Locations created: {len(locations)}")