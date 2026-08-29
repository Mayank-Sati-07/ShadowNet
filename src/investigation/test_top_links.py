from src.investigation.investigation_engine import InvestigationEngine


def main():

    print("=" * 70)
    print("CNAS TOP-K LINK PREDICTION")
    print("=" * 70)

    engine = InvestigationEngine()

    try:

        person_id = "SYN_P_0001"

        print(
            f"\nTarget Person: {person_id}"
        )

        results = engine.rank_link_predictions(
            person_id,
            limit=10
        )

        if not results:

            print("\nNo candidate links found.")

            return

        print("\n" + "-" * 70)
        print("TOP PREDICTED CONNECTIONS")
        print("-" * 70)

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n#{index}"
            )

            print(
                f"Person: "
                f"{result['person_b']}"
            )

            print(
                f"Jaccard: "
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