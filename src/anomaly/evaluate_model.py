from src.anomaly.load_transactions import load_transactions
from src.anomaly.feature_engineering import (
    clean_transactions,
    create_features,
)
from src.anomaly.isolation_forest import (
    run_isolation_forest,
)

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


def main():

    print("=" * 70)
    print("CNAS ANOMALY MODEL EVALUATION")
    print("=" * 70)

    # Load
    df = load_transactions()

    # Clean
    df = clean_transactions(df)

    # Features
    df = create_features(df)

    # Model
    df, model = run_isolation_forest(df)

    # Ground truth
    y_true = df["is_anomaly"].astype(int)

    # Prediction
    y_pred = df["model_prediction"].astype(int)

    print("\nConfusion Matrix:")

    matrix = confusion_matrix(
        y_true,
        y_pred,
    )

    print(matrix)

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            y_pred,
            digits=4,
            zero_division=0,
        )
    )

    print("\nKey Metrics:")

    print(
        f"Precision: "
        f"{precision_score(y_true, y_pred, zero_division=0):.4f}"
    )

    print(
        f"Recall:    "
        f"{recall_score(y_true, y_pred, zero_division=0):.4f}"
    )

    print(
        f"F1 Score:  "
        f"{f1_score(y_true, y_pred, zero_division=0):.4f}"
    )


if __name__ == "__main__":
    main()