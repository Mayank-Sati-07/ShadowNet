from src.investigation.investigation_engine import InvestigationEngine


def main():

    person_id = "SYN_P_0001"

    print("=" * 70)
    print("CNAS INVESTIGATION PATH TEST")
    print("=" * 70)

    engine = InvestigationEngine()

    try:

        paths = engine.get_investigation_paths(
            person_id,
            limit=10
        )

        print(f"\nPerson: {person_id}")
        print(f"Paths returned: {len(paths)}")

        for i, path in enumerate(paths, 1):

            print(f"\nPath {i}:")
            print(path)

    finally:

        engine.close()


if __name__ == "__main__":
    main()