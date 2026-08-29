class AnomalyAgent:

    def __init__(self, model):

        self.model = model

    def investigate(self, features):

        predictions, scores = (
            self.model.predict(features)
        )

        results = []

        for prediction, score in zip(
            predictions,
            scores
        ):

            results.append({

                "is_anomaly": prediction == -1,

                "anomaly_score": float(score)

            })

        return results