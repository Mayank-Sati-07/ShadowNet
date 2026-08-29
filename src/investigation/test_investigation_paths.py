from src.investigation.investigation_engine import InvestigationEngine


def main():

    person_id = "SYN_P_0001"

    print("=" * 70)
    print("CNAS INVESTIGATION PATH TEST")
    print("=" * 70)

    print(f"\nInvestigating paths for: {person_id}")

    engine = InvestigationEngine()

    try:

        paths = engine.get_investigation_paths(
            person_id,
            limit=10
        )

        print("\n✓ Investigation path query executed")

        print("\nPaths returned:", len(paths))

        print("\n" + "-" * 70)
        print("PATHS")
        print("-" * 70)

        for i, path in enumerate(paths, start=1):

            print(f"\nPath {i}:")
            print(path)

        print("\n" + "=" * 70)
        print("✓ INVESTIGATION PATH TEST COMPLETED")
        print("=" * 70)

    except Exception as e:

        print("\n✗ Investigation path test failed")
        print("Error:", e)

    finally:

        engine.close()


if __name__ == "__main__":
    main()
