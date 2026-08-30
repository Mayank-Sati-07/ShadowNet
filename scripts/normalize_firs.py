from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "source_fir_records_cleaned.csv"
)

firs = pd.DataFrame({
    "fir_id": df["fir_id"],
    "record_uid": df["record_uid"],
    "image_id": df["image_id"],
    "station_id": df["station_id"],
    "date": pd.to_datetime(
        df["year"],
        format="%Y",
        errors="coerce"
    ),
    "year": df["year"],
    "crime_type": df["primary_act"],
    "acts_list": df["acts_list"],
    "sections_list": df["sections_list"],
    "completeness_pct": df["completeness_pct"],
    "confidence": df["avg_confidence"],
    "source": df["data_provenance"]
})

firs.to_csv(
    OUT_DIR / "firs.csv",
    index=False
)

print(f"FIRs created: {len(firs)}")