def generate_reason(row, df):

    reasons = []

    # ==================================================
    # HIGH ABSOLUTE AMOUNT
    # ==================================================

    amount_95 = (
        df["amount"]
        .quantile(0.95)
    )

    if row["amount"] >= amount_95:

        reasons.append(
            "transaction amount is unusually high"
        )

    # ==================================================
    # PERSON RELATIVE AMOUNT
    # ==================================================

    if (
        row.get(
            "amount_vs_person_mean",
            0
        ) >= 3
    ):

        reasons.append(
            "amount is more than 3x "
            "the person's average"
        )

    # ==================================================
    # AMOUNT Z-SCORE
    # ==================================================

    if (
        row.get(
            "amount_zscore",
            0
        ) >= 3
    ):

        reasons.append(
            "amount is an extreme deviation "
            "from the person's historical behavior"
        )

    # ==================================================
    # DAILY TOTAL
    # ==================================================

    daily_95 = (
        df["daily_total"]
        .quantile(0.95)
    )

    if (
        row["daily_total"]
        >= daily_95
    ):

        reasons.append(
            "daily transaction total is unusually high"
        )

    # ==================================================
    # HIGH FREQUENCY
    # ==================================================

    frequency_95 = (
        df["transaction_frequency"]
        .quantile(0.95)
    )

    if (
        row["transaction_frequency"]
        >= frequency_95
    ):

        reasons.append(
            "transaction frequency is unusually high"
        )

    # ==================================================
    # MANY TARGETS
    # ==================================================

    accounts_95 = (
        df["unique_accounts"]
        .quantile(0.95)
    )

    if (
        row["unique_accounts"]
        >= accounts_95
    ):

        reasons.append(
            "person interacts with an unusually "
            "large number of accounts"
        )

    # ==================================================
    # NIGHT
    # ==================================================

    if (
        row.get(
            "is_night",
            0
        ) == 1
    ):

        reasons.append(
            "transaction occurred during unusual hours"
        )

    # ==================================================
    # SOURCE AMOUNT RATIO
    # ==================================================

    if (
        row.get(
            "source_amount_ratio",
            0
        ) >= 3
    ):

        reasons.append(
            "amount is unusually high relative "
            "to source historical behavior"
        )

    # ==================================================
    # FALLBACK
    # ==================================================

    if not reasons:

        reasons.append(
            "transaction differs from the learned "
            "behavioral pattern"
        )

    return "; ".join(reasons)