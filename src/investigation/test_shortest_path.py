from src.investigation.investigation_engine import InvestigationEngine


def main():

    print("=" * 70)
    print("ShadowNet SHORTEST PATH TEST")
    print("=" * 70)

    engine = InvestigationEngine()

    try:

        person_a = "SYN_P_0001"
        person_b = "SYN_P_0002"

        print(f"\nPerson A: {person_a}")
        print(f"Person B: {person_b}")

        result = engine.get_shortest_path(
            person_a,
            person_b
        )

        if not result:

            print("\nNo path found.")

            return

        print("\nShortest path:")

        for path in result:

            print(
                f"\nNodes: "
                f"{path['nodes']}"
            )

            print(
                f"Labels: "
                f"{path['node_labels']}"
            )

            print(
                f"Relationships: "
                f"{path['relationships']}"
            )

            print(
                f"Distance: "
                f"{path['distance']}"
            )

    finally:

        engine.close()


if __name__ == "__main__":
    main()