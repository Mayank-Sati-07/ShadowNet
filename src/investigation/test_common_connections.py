from src.investigation.investigation_engine import InvestigationEngine


def main():

    print("=" * 70)
    print("CNAS COMMON CONNECTION TEST")
    print("=" * 70)

    engine = InvestigationEngine()

    try:

        person_a = "SYN_P_0001"
        person_b = "SYN_P_0002"

        print(f"\nPerson A: {person_a}")
        print(f"Person B: {person_b}")

        results = engine.get_common_connections(
            person_a,
            person_b
        )

        if not results:

            print("\nNo common connections found.")

            return

        print(
            f"\nFound {len(results)} common connection(s):"
        )

        for result in results:

            print("\n--------------------------------")

            print(
                f"Entity: "
                f"{result['common_entity']}"
            )

            print(
                f"Labels: "
                f"{result['entity_labels']}"
            )

            print(
                f"A relationship: "
                f"{result['relationship_from_a']}"
            )

            print(
                f"B relationship: "
                f"{result['relationship_to_b']}"
            )

    finally:

        engine.close()


if __name__ == "__main__":
    main()