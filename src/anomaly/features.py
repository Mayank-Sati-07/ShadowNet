import pandas as pd


def build_transaction_features(
    transactions: pd.DataFrame
):

    df = transactions.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["amount_log"] = (
        df["amount"]
        .clip(lower=0)
        .apply(lambda x: __import__("math").log1p(x))
    )

    df["transaction_frequency"] = (
        df.groupby("source_account")[
            "source_account"
        ].transform("count")
    )

    df["unique_targets"] = (
        df.groupby("source_account")[
            "target_account"
        ].transform("nunique")
    )

    return df