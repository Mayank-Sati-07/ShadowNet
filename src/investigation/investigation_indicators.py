def calculate_indicators(result):

    network = result["network"]
    transactions = result["transactions"]
    community = result["community"]

    indicators = []

    # --------------------------------------------------------
    # Network indicators
    # --------------------------------------------------------

    if network["direct_connections"] >= 30:

        indicators.append({
            "category": "network",
            "type": "high_connectivity",
            "description":
                "Person has a relatively large number "
                "of direct network connections.",
        })

    # --------------------------------------------------------
    # Financial / anomaly indicators
    # --------------------------------------------------------

    if transactions["anomalous_count"] >= 3:

        indicators.append({
            "category": "financial",
            "type": "multiple_transaction_anomalies",
            "description":
                "Multiple transactions associated "
                "with this person were flagged by "
                "the anomaly detection model.",
        })

    # --------------------------------------------------------
    # Community indicators
    # --------------------------------------------------------

    if community["community_id"] is not None:

        indicators.append({
            "category": "community",
            "type": "community_membership",
            "description":
                "Person belongs to a detected "
                "network community.",
        })

    return indicators