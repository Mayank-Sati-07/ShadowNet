from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "synthetic_transactions.csv"
)

transactions = pd.DataFrame({
    "relationship_id": df["transaction_id"],
    "source_id": df["sender_id"],
    "source_type": "Person",
    "relationship": "TRANSFERRED_MONEY",
    "target_id": df["receiver_id"],
    "target_type": "Person",
    "timestamp": df["timestamp"],
    "source_document": pd.NA,
    "confidence": 1.0,
    "provenance": df["data_provenance"],
    "amount": df["amount"],
    "channel": df["channel"],
    "is_anomaly": df["is_injected_anomaly"],
    "anomaly_type": df["anomaly_type"]
})

transactions.to_csv(
    OUT_DIR / "relationships_transactions.csv",
    index=False
)