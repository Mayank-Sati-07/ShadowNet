from src.investigation.investigation_engine import InvestigationEngine


def main():

    print("=" * 70)
    print("ShadowNet LINK PREDICTION TEST")
    print("=" * 70)

    engine = InvestigationEngine()

    try:

        person_a = "SYN_P_0001"
        person_b = "SYN_P_0002"

        print(f"\nPerson A: {person_a}")
        print(f"Person B: {person_b}")

        # ------------------------------------------------
        # Jaccard
        # ------------------------------------------------

        jaccard = engine.calculate_jaccard(
            person_a,
            person_b
        )

        # ------------------------------------------------
        # Common neighbors
        # ------------------------------------------------

        common_neighbors = engine.get_common_neighbors(
            person_a,
            person_b
        )

        # ------------------------------------------------
        # Adamic-Adar
        # ------------------------------------------------

        adamic_adar = engine.calculate_adamic_adar(
            person_a,
            person_b
        )

        print("\n" + "-" * 70)
        print("GRAPH SIMILARITY FEATURES")
        print("-" * 70)

        print(
            f"\nCommon neighbors: "
            f"{common_neighbors}"
        )

        print(
            f"Total unique neighbors: "
            f"{jaccard['union_size']}"
        )

        print(
            f"Jaccard score: "
            f"{jaccard['jaccard_score']:.4f}"
        )

        print(
            f"Adamic-Adar score: "
            f"{adamic_adar:.4f}"
        )

    finally:

        engine.close()


if __name__ == "__main__":
    main()