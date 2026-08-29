import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "amount",
    "transaction_frequency",
    "daily_total",
    "unique_accounts",
    "time_of_day",
]


def run_isolation_forest(df: pd.DataFrame):

    df = df.copy()

    # -------------------------------------------------
    # Validate features
    # -------------------------------------------------

    missing_features = [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            "Missing features: "
            + ", ".join(missing_features)
        )

    # -------------------------------------------------
    # Prepare model input
    # -------------------------------------------------

    X = (
        df[FEATURE_COLUMNS]
        .apply(pd.to_numeric, errors="coerce")
        .replace([float("inf"), float("-inf")], pd.NA)
        .fillna(0.0)
    )

    # -------------------------------------------------
    # Isolation Forest
    # -------------------------------------------------

    model = IsolationForest(
        n_estimators=300,
        contamination="auto",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X)

    # -------------------------------------------------
    # Predictions
    #
    #  1  = normal
    # -1  = anomaly
    # -------------------------------------------------

    predictions = model.predict(X)

    # -------------------------------------------------
    # sklearn decision score
    #
    # Higher = more normal
    # Lower  = more anomalous
    # -------------------------------------------------

    raw_scores = model.decision_function(X)

    # -------------------------------------------------
    # Convert to:
    #
    # 0 = normal
    # 1 = highly anomalous
    # -------------------------------------------------

    min_score = raw_scores.min()
    max_score = raw_scores.max()

    if max_score == min_score:

        anomaly_scores = pd.Series(
            0.0,
            index=df.index
        )

    else:

        anomaly_scores = (
            1
            - (
                (raw_scores - min_score)
                / (max_score - min_score)
            )
        )

    # -------------------------------------------------
    # Store results
    # -------------------------------------------------

    df["model_prediction"] = (
        predictions == -1
    ).astype(int)

    df["is_anomaly"] = (
        df["model_prediction"] == 1
    )

    df["raw_anomaly_score"] = raw_scores

    df["anomaly_score"] = anomaly_scores

    return df, model
