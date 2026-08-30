import pandas as pd
import numpy as np


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw transaction relationship data.
    """

    df = df.copy()

    required_columns = [
        "relationship_id",
        "source_id",
        "target_id",
        "timestamp",
        "amount",
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # --------------------------------------------------
    # Transaction ID
    # --------------------------------------------------

    df["transaction_id"] = (
        df["relationship_id"]
        .astype(str)
    )

    # --------------------------------------------------
    # Person ID
    # --------------------------------------------------

    df["person_id"] = (
        df["source_id"]
        .astype(str)
    )

    # --------------------------------------------------
    # Timestamp
    # --------------------------------------------------

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # --------------------------------------------------
    # Amount
    # --------------------------------------------------

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove invalid timestamps
    df = df.dropna(
        subset=[
            "timestamp",
            "amount"
        ]
    ).copy()

    # Negative transaction amounts are invalid
    df = df[
        df["amount"] >= 0
    ].copy()

    df = df.reset_index(drop=True)

    print(
        f"[OK] Clean transactions: {len(df):,}"
    )

    return df


def create_transaction_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Create transaction-level behavioral features.
    """

    df = df.copy()

    # ==================================================
    # TIME FEATURES
    # ==================================================

    df["hour"] = (
        df["timestamp"]
        .dt.hour
    )

    df["day_of_week"] = (
        df["timestamp"]
        .dt.dayofweek
    )

    df["date"] = (
        df["timestamp"]
        .dt.date
    )

    # --------------------------------------------------
    # Unusual transaction hours
    #
    # 00:00 - 05:59
    # --------------------------------------------------

    df["time_of_day"] = (
        df["hour"]
        .between(0, 5)
        .astype(int)
    )

    # Better explicit night indicator
    df["is_night"] = (
        df["hour"]
        .between(0, 5)
        .astype(int)
    )

    # ==================================================
    # PERSON TRANSACTION FREQUENCY
    # ==================================================

    person_counts = (
        df.groupby("person_id")
        .size()
    )

    df["transaction_frequency"] = (
        df["person_id"]
        .map(person_counts)
        .fillna(0)
    )

    # ==================================================
    # DAILY TOTAL
    # ==================================================

    daily_totals = (
        df.groupby(
            [
                "person_id",
                "date"
            ]
        )["amount"]
        .sum()
    )

    df["daily_total"] = [
        daily_totals.get(
            (person, date),
            0
        )
        for person, date in zip(
            df["person_id"],
            df["date"]
        )
    ]

    # ==================================================
    # UNIQUE ACCOUNTS / TARGETS
    # ==================================================

    unique_targets = (
        df.groupby("person_id")["target_id"]
        .nunique()
    )

    df["unique_accounts"] = (
        df["person_id"]
        .map(unique_targets)
        .fillna(0)
    )

    # ==================================================
    # PERSON MEAN AMOUNT
    # ==================================================

    person_mean = (
        df.groupby("person_id")["amount"]
        .transform("mean")
    )

    df["amount_vs_person_mean"] = (
        df["amount"]
        / person_mean.replace(0, np.nan)
    ).fillna(1.0)

    # ==================================================
    # AMOUNT RANK
    # ==================================================

    df["amount_rank"] = (
        df["amount"]
        .rank(
            pct=True
        )
    )

    # ==================================================
    # Z-SCORE OF TRANSACTION AMOUNT
    # ==================================================

    person_std = (
        df.groupby("person_id")["amount"]
        .transform("std")
    )

    person_mean = (
        df.groupby("person_id")["amount"]
        .transform("mean")
    )

    df["amount_zscore"] = (
        (
            df["amount"]
            - person_mean
        )
        /
        person_std.replace(
            0,
            np.nan
        )
    ).fillna(0)

    # ==================================================
    # SOURCE TRANSACTION COUNT
    # ==================================================

    source_transaction_count = (
        df.groupby("source_id")
        .size()
    )

    df["source_transaction_count"] = (
        df["source_id"]
        .map(
            source_transaction_count
        )
        .fillna(0)
    )

    # ==================================================
    # SOURCE MEAN AMOUNT
    # ==================================================

    source_mean_amount = (
        df.groupby("source_id")["amount"]
        .transform("mean")
    )

    df["source_mean_amount"] = (
        source_mean_amount
        .fillna(0)
    )

    # ==================================================
    # SOURCE AMOUNT RATIO
    # ==================================================

    df["source_amount_ratio"] = (
        df["amount"]
        /
        df["source_mean_amount"]
        .replace(0, np.nan)
    ).fillna(1.0)

    # ==================================================
    # SAFETY CLEANUP
    # ==================================================

    numeric_columns = [
        "amount",
        "transaction_frequency",
        "daily_total",
        "unique_accounts",
        "amount_vs_person_mean",
        "amount_rank",
        "amount_zscore",
        "source_transaction_count",
        "source_mean_amount",
        "source_amount_ratio",
        "hour",
        "day_of_week",
        "time_of_day",
        "is_night",
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .replace(
                    [np.inf, -np.inf],
                    np.nan
                )
                .fillna(0)
            )

    print(
        f"[OK] Feature dataframe: "
        f"{len(df):,} rows"
    )

    return df


# Backward-compatible alias
#
# Your run_anomaly_detection.py imports
# create_features, while test_features.py
# uses create_transaction_features.
#
# This avoids the import error.
def create_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    return create_transaction_features(df)