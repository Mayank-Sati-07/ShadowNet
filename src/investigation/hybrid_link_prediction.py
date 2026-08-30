import math

from src.investigation.investigation_engine import InvestigationEngine
from src.investigation.node2vec import ShadowNetNode2Vec


class HybridLinkPredictor:

    def __init__(self):

        self.engine = InvestigationEngine()

        self.node2vec = ShadowNetNode2Vec(
            dimensions=128,
            walk_length=30,
            num_walks=100,
            workers=4,
            window=10,
        )

    # --------------------------------------------------
    # Normalize value
    # --------------------------------------------------

    @staticmethod
    def min_max_normalize(
        value,
        minimum,
        maximum
    ):

        if maximum == minimum:

            return 0.0

        return (
            (value - minimum)
            / (maximum - minimum)
        )

    # --------------------------------------------------
    # Calculate hybrid score
    # --------------------------------------------------

    def calculate_score(
        self,
        person_a,
        person_b,
        adamic_min,
        adamic_max,
    ):

        # ----------------------------------------------
        # Jaccard
        # ----------------------------------------------

        jaccard_result = (
            self.engine.calculate_jaccard(
                person_a,
                person_b
            )
        )

        if isinstance(jaccard_result, dict):

            jaccard = float(
                jaccard_result.get(
                    "jaccard_score",
                    0.0
                )
            )

        else:

            jaccard = float(
                jaccard_result
            )

        # ----------------------------------------------
        # Adamic-Adar
        # ----------------------------------------------

        adamic_result = (
            self.engine.calculate_adamic_adar(
                person_a,
                person_b
            )
        )

        if isinstance(adamic_result, dict):

            adamic_adar = float(
                adamic_result.get(
                    "adamic_adar_score",
                    0.0
                )
            )

        else:

            adamic_adar = float(
                adamic_result
            )

        adamic_normalized = (
            self.min_max_normalize(
                adamic_adar,
                adamic_min,
                adamic_max
            )
        )

        # ----------------------------------------------
        # Node2Vec
        # ----------------------------------------------

        node2vec_similarity = (
            self.node2vec.similarity(
                person_a,
                person_b
            )
        )

        if node2vec_similarity is None:

            node2vec_similarity = 0.0

        # Node2Vec cosine similarity can be
        # [-1, 1].
        #
        # Convert it to [0, 1].

        node2vec_normalized = (
            node2vec_similarity + 1.0
        ) / 2.0

        # ----------------------------------------------
        # Hybrid score
        # ----------------------------------------------

        hybrid_score = (

            0.25 * jaccard

            + 0.35 * adamic_normalized

            + 0.40 * node2vec_normalized
        )

        return {

            "person_a": person_a,

            "person_b": person_b,

            "jaccard": jaccard,

            "adamic_adar": adamic_adar,

            "adamic_adar_normalized":
                adamic_normalized,

            "node2vec_similarity":
                node2vec_similarity,

            "node2vec_normalized":
                node2vec_normalized,

            "hybrid_score":
                hybrid_score,
        }

    # --------------------------------------------------
    # Train Node2Vec
    # --------------------------------------------------

    def train(self):

        graph = self.node2vec.load_person_graph()

        self.node2vec.train(graph)

    # --------------------------------------------------
    # Close
    # --------------------------------------------------

    def close(self):

        self.node2vec.close()

        self.engine.close()