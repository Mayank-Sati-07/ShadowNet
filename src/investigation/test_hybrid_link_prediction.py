from src.investigation.hybrid_link_prediction import HybridLinkPredictor


def main():

    print("=" * 70)
    print("ShadowNet HYBRID LINK PREDICTION TEST")
    print("=" * 70)

    person_a = "SYN_P_0001"
    person_b = "SYN_P_0002"

    predictor = HybridLinkPredictor()

    try:

        print(f"\nPerson A: {person_a}")
        print(f"Person B: {person_b}")

        # --------------------------------------------------
        # Train Node2Vec
        # --------------------------------------------------

        predictor.train()

        # --------------------------------------------------
        # Calculate hybrid score
        # --------------------------------------------------

        print("\nCalculating hybrid score...")

        result = predictor.calculate_score(
            person_a,
            person_b,
            adamic_min=0.0,
            adamic_max=10.0,
        )

        if result is None:

            print("\n⚠ Could not calculate hybrid score.")

            return

        # --------------------------------------------------
        # Display results
        # --------------------------------------------------

        print("\n" + "-" * 70)
        print("HYBRID LINK PREDICTION RESULT")
        print("-" * 70)

        print(
            f"\nJaccard: "
            f"{result['jaccard']:.4f}"
        )

        print(
            f"Adamic-Adar: "
            f"{result['adamic_adar']:.4f}"
        )

        print(
            f"Adamic-Adar normalized: "
            f"{result['adamic_adar_normalized']:.4f}"
        )

        print(
            f"Node2Vec similarity: "
            f"{result['node2vec_similarity']:.4f}"
        )

        print(
            f"Node2Vec normalized: "
            f"{result['node2vec_normalized']:.4f}"
        )

        print(
            f"\nHybrid Score: "
            f"{result['hybrid_score']:.4f}"
        )

        print("\n" + "-" * 70)

    finally:

        predictor.close()


if __name__ == "__main__":
    main()