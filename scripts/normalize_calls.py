from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_calls.csv"
)

calls = pd.DataFrame({
    "relationship_id": df["call_id"],
    "source_id": df["caller_id"],
    "source_type": "Person",
    "relationship": "CALLED",
    "target_id": df["receiver_id"],
    "target_type": "Person",
    "timestamp": df["timestamp"],
    "source_document": pd.NA,
    "confidence": 1.0,
    "provenance": df["data_provenance"],
    "duration_sec": df["duration_sec"],
    "communication_type": df["communication_type"]
})

calls.to_csv(
    OUT_DIR / "relationships_calls.csv",
    index=False
)

print(f"Calls created: {len(calls)}")