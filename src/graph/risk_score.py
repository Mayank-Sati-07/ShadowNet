class InvestigationScorer:

    @staticmethod
    def calculate(
        degree,
        betweenness,
        anomaly_count,
        document_mentions
    ):

        score = (

            min(degree / 100, 1.0) * 0.30

            +

            min(betweenness, 1.0) * 0.30

            +

            min(anomaly_count / 10, 1.0) * 0.25

            +

            min(document_mentions / 10, 1.0) * 0.15

        )

        return round(
            score * 100,
            2
        )

def classify_score(score):

    if score >= 80:
        return "CRITICAL"

    if score >= 60:
        return "HIGH"

    if score >= 40:
        return "MEDIUM"

    return "LOW"