from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_emails.csv"
)

emails = pd.DataFrame({
    "relationship_id": df["email_id"],
    "source_id": df["sender_id"],
    "source_type": "Person",
    "relationship": "EMAILED",
    "target_id": df["receiver_id"],
    "target_type": "Person",
    "timestamp": pd.NA,
    "source_document": pd.NA,
    "confidence": 1.0,
    "provenance": df["data_provenance"]
})

emails.to_csv(
    OUT_DIR / "relationships_emails.csv",
    index=False
)