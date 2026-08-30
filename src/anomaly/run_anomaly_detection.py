from pathlib import Path

from src.anomaly.load_transactions import load_transactions

from src.anomaly.feature_engineering import (
    clean_transactions,
    create_features,
)

from src.anomaly.isolation_forest import (
    run_isolation_forest,
)

from src.anomaly.anomaly_reasons import (
    generate_reason,
)

from src.anomaly.save_anomalies import (
    save_anomalies,
)


OUTPUT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "transaction_anomalies.csv"
)


def main():

    print("=" * 70)
    print("ShadowNet TRANSACTION ANOMALY DETECTION")
    print("=" * 70)

    # =================================================
    # 1. LOAD
    # =================================================

    print("\n[1/5] Loading transactions...")

    df = load_transactions()

    # =================================================
    # 2. CLEAN
    # =================================================

    print("\n[2/5] Cleaning transactions...")

    df = clean_transactions(df)

    print(
        f"Valid transactions: {len(df):,}"
    )

    # =================================================
    # 3. FEATURES
    # =================================================

    print("\n[3/5] Creating features...")

    df = create_features(df)

    important_features = [
        "amount",
        "transaction_frequency",
        "daily_total",
        "unique_accounts",
        "time_of_day",
        "amount_vs_person_mean",
        "amount_zscore",
        "source_transaction_count",
        "source_mean_amount",
        "source_amount_ratio",
        "is_night",
    ]

    print("\nFeatures created:")

    for feature in important_features:

        if feature in df.columns:
            print(f"  [OK] {feature}")
        else:
            print(f"  - {feature} not used by current feature pipeline")

    # =================================================
    # 4. ISOLATION FOREST
    # =================================================

    print(
        "\n[4/5] Running Isolation Forest..."
    )

    df, model = run_isolation_forest(df)

    # =================================================
    # 5. EXPLANATIONS
    # =================================================

    print(
        "\n[5/5] Generating explanations..."
    )

    df["reason"] = df.apply(
        lambda row: generate_reason(row, df),
        axis=1,
    )

    # =================================================
    # SORT
    # =================================================

    df = df.sort_values(
        "anomaly_score",
        ascending=False,
    ).reset_index(drop=True)

    # =================================================
    # SAVE COMPLETE DATASET
    # =================================================

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    # =================================================
    # RESULTS
    # =================================================

    total_count = len(df)

    model_anomalies = int(
        df["model_prediction"].sum()
    )

    normal_count = (
        total_count - model_anomalies
    )

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)

    print(
        f"Total transactions : {total_count:,}"
    )

    print(
        f"Model anomalies    : {model_anomalies:,}"
    )

    print(
        f"Normal transactions: {normal_count:,}"
    )

    if total_count:

        print(
            f"Anomaly percentage : "
            f"{model_anomalies / total_count * 100:.2f}%"
        )

    # =================================================
    # GROUND TRUTH
    # =================================================

    if "is_anomaly" in df.columns:

        ground_truth = int(
            df["is_anomaly"].sum()
        )

        print(
            f"Ground truth anomalies: "
            f"{ground_truth:,}"
        )

    # =================================================
    # OUTPUT
    # =================================================

    print("\nSaved to:")
    print(OUTPUT_FILE)

    # =================================================
    # TOP SUSPICIOUS TRANSACTIONS
    # =================================================

    print(
        "\nTop suspicious transactions:"
    )

    suspicious = df[
        df["model_prediction"] == 1
    ].head(20)

    columns = [
        "transaction_id",
        "person_id",
        "amount",
        "anomaly_score",
        "model_prediction",
        "reason",
    ]

    columns = [
        column
        for column in columns
        if column in suspicious.columns
    ]

    if len(suspicious):

        print(
            suspicious[columns]
            .to_string(index=False)
        )

    else:

        print(
            "No anomalies detected."
        )

    # =================================================
    # SAVE ALERTS
    # =================================================

    alerts = df[
        df["model_prediction"] == 1
    ].copy()

    if len(alerts):

        save_anomalies(alerts)

        print(
            f"\n[OK] Saved {len(alerts):,} anomaly alerts"
        )

    else:

        print(
            "\n[OK] No anomaly alerts to save"
        )

    print(
        "\n[OK] ShadowNet anomaly detection completed"
    )


if __name__ == "__main__":
    main()
