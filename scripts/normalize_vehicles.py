from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_vehicles.csv"
)

vehicles = pd.DataFrame({
    "vehicle_id": df["vehicle_id"],
    "vehicle_type": df["vehicle_type"],
    "source": df["data_provenance"]
})

vehicles = vehicles.drop_duplicates(
    subset=["vehicle_id"]
)

vehicles.to_csv(
    OUT_DIR / "vehicles.csv",
    index=False
)

print(f"Vehicles created: {len(vehicles)}")