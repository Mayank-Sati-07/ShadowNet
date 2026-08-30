class LinkPredictionScorer:
    """
    Combines graph-based similarity features
    into a single link prediction score.
    """

    def __init__(
        self,
        jaccard_weight=0.4,
        adamic_adar_weight=0.6
    ):
        self.jaccard_weight = jaccard_weight
        self.adamic_adar_weight = adamic_adar_weight

    # --------------------------------------------------
    # Min-Max normalization
    # --------------------------------------------------

    @staticmethod
    def normalize(value, minimum, maximum):

        if maximum == minimum:
            return 0.0

        return (value - minimum) / (maximum - minimum)

    # --------------------------------------------------
    # Combined score
    # --------------------------------------------------

    def combined_score(
        self,
        jaccard,
        adamic_adar,
        max_adamic_adar=10.0
    ):

        normalized_jaccard = self.normalize(
            jaccard,
            0.0,
            1.0
        )

        normalized_adamic_adar = self.normalize(
            adamic_adar,
            0.0,
            max_adamic_adar
        )

        score = (
            self.jaccard_weight * normalized_jaccard
            +
            self.adamic_adar_weight * normalized_adamic_adar
        )

        return min(max(score, 0.0), 1.0)