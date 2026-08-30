from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_visits.csv"
)

visits = pd.DataFrame({
    "relationship_id": df["visit_id"],
    "source_id": df["person_id"],
    "source_type": "Person",
    "relationship": "VISITED",
    "target_id": df["location_id"],
    "target_type": "Location",
    "timestamp": df["timestamp"],
    "source_document": pd.NA,
    "confidence": 1.0,
    "provenance": df["data_provenance"],
    "is_anomaly": df["is_injected_anomaly"],
    "anomaly_type": df["anomaly_type"]
})

visits.to_csv(
    OUT_DIR / "relationships_visits.csv",
    index=False
)