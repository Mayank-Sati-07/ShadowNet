from sklearn.ensemble import IsolationForest


class TransactionAnomalyModel:

    def __init__(self):

        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.05,
            random_state=42
        )

    def fit(self, X):

        self.model.fit(X)

    def predict(self, X):

        predictions = self.model.predict(X)

        scores = -self.model.score_samples(X)

        return predictions, scores