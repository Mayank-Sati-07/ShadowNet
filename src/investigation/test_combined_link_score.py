from src.investigation.investigation_engine import InvestigationEngine


def main():

    print("=" * 70)
    print("ShadowNet COMBINED LINK PREDICTION TEST")
    print("=" * 70)

    engine = InvestigationEngine()

    try:

        person_a = "SYN_P_0001"
        person_b = "SYN_P_0002"

        print(f"\nPerson A: {person_a}")
        print(f"Person B: {person_b}")

        result = engine.calculate_combined_link_score(
            person_a,
            person_b
        )

        if not result:

            print("\nNo result found.")

            return

        print("\n" + "-" * 70)
        print("LINK PREDICTION FEATURES")
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
            f"Combined Score: "
            f"{result['combined_score']:.4f}"
        )

    finally:

        engine.close()


if __name__ == "__main__":
    main()