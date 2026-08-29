from src.investigation.investigation_engine import InvestigationEngine


def main():

    print("=" * 70)
    print("CNAS CANDIDATE GENERATION VALIDATION")
    print("=" * 70)

    person_id = "SYN_P_0001"

    engine = InvestigationEngine()

    try:

        candidates = (
            engine.generate_link_prediction_candidates(
                person_id,
                limit=100
            )
        )

        print(
            f"\nTarget: {person_id}"
        )

        print(
            f"Candidates: {len(candidates)}"
        )

        invalid = []

        for candidate in candidates:

            connected = (
                engine.is_directly_connected(
                    person_id,
                    candidate
                )
            )

            if connected:

                invalid.append(candidate)

        print("\n" + "-" * 70)
        print("VALIDATION")
        print("-" * 70)

        print(
            f"Total candidates: "
            f"{len(candidates)}"
        )

        print(
            f"Existing direct connections: "
            f"{len(invalid)}"
        )

        if len(invalid) == 0:

            print(
                "✓ PASS: No candidate has "
                "an existing direct relationship"
            )

        else:

            print(
                "✗ FAIL: Invalid candidates found"
            )

            for candidate in invalid:

                print(
                    f"  - {candidate}"
                )

    finally:

        engine.close()


if __name__ == "__main__":
    main()