from src.investigation.investigation_engine import (
    InvestigationEngine
)


def main():

    print("=" * 70)
    print("CNAS INVESTIGATION ENGINE TEST")
    print("=" * 70)

    person_id = "SYN_P_0001"

    print(
        f"\nInvestigating: {person_id}"
    )

    engine = InvestigationEngine()

    try:

        result = engine.investigate(
            person_id
        )

        print("\nRESULT KEYS:")
        print(result.keys())
        # ----------------------------------------------------
        # Investigation validation
        # ----------------------------------------------------

        if not result["success"]:

            print(
                "\n✗ Investigation failed"
            )

            print(
                result["error"]
            )

            return

        print(
            "\n✓ Investigation completed"
        )

        # ----------------------------------------------------
        # Network
        # ----------------------------------------------------

        network = result["network"]

        print("\n" + "-" * 70)
        print("NETWORK")
        print("-" * 70)

        print(
            "Direct connections:",
            network["direct_connections"]
        )

        print(
            "Relationships:",
            network["relationship_count"]
        )

        print(
            "2-hop connections:",
            network["two_hop_connections"]
        )

        # ----------------------------------------------------
        # Entities
        # ----------------------------------------------------

        entities = result["entities"]

        print("\n" + "-" * 70)
        print("CONNECTED ENTITIES")
        print("-" * 70)

        print(
            "Phones:",
            len(entities["phones"])
        )

        print(
            "Vehicles:",
            len(entities["vehicles"])
        )

        print(
            "Accounts:",
            len(entities["accounts"])
        )

        print(
            "Locations:",
            len(entities["locations"])
        )

        print(
            "Organizations:",
            len(entities["organizations"])
        )

        print(
            "FIRs:",
            len(entities["firs"])
        )

        # ----------------------------------------------------
        # Transactions
        # ----------------------------------------------------

        transactions = result["transactions"]

        print("\n" + "-" * 70)
        print("TRANSACTIONS")
        print("-" * 70)

        print(
            "Total:",
            transactions["total"]
        )

        print(
            "Anomalous:",
            transactions["anomalous_count"]
        )

        # ----------------------------------------------------
        # Community
        # ----------------------------------------------------

        community = result["community"]

        print("\n" + "-" * 70)
        print("COMMUNITY")
        print("-" * 70)

        print(
            "Community ID:",
            community["community_id"]
        )

        print(
            "Community size:",
            community["community_size"]
        )

        print(
            "Important people:",
            len(
                community["important_people"]
            )
        )

        # ----------------------------------------------------
        # Connected people
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("CONNECTED PEOPLE")
        print("-" * 70)

        for person in network["connected_people"][:20]:

            print(
                person
            )

        # ----------------------------------------------------
        # Investigation Indicators
        # ----------------------------------------------------

        indicators = result["indicators"]

        print("\n" + "-" * 70)
        print("INVESTIGATION INDICATORS")
        print("-" * 70)

        if not indicators:

            print(
                "No indicators detected."
            )

        else:

            for indicator in indicators:

                print(
                    f"\n[{indicator['category']}] "
                    f"{indicator['type']}"
                )

                print(
                    "Description:",
                    indicator["description"]
                )

                # Optional values
                if "value" in indicator:

                    print(
                        "Value:",
                        indicator["value"]
                    )

                if "community_id" in indicator:

                    print(
                        "Community ID:",
                        indicator["community_id"]
                    )

                if "community_size" in indicator:

                    print(
                        "Community size:",
                        indicator["community_size"]
                    )

        # ----------------------------------------------------
        # Final success
        # ----------------------------------------------------

        print("\n" + "=" * 70)
        print("✓ INVESTIGATION TEST COMPLETED")
        print("=" * 70)

    finally:

        engine.close()


if __name__ == "__main__":

    main()
