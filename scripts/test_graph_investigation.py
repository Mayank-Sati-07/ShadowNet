from src.graph.investigation_service import (
    GraphInvestigationService
)


def main():

    service = GraphInvestigationService()

    print("=" * 70)
    print("CNAS GRAPH INVESTIGATION")
    print("=" * 70)

    # ---------------------------------------------------------
    # Find Raj Kumar
    # ---------------------------------------------------------

    persons = service.find_person(
        "Raj Kumar"
    )

    print("\nRaj Kumar:")

    for person in persons:

        print(person)

    if not persons:
        print(
            "Raj Kumar not found"
        )
        return

    person_id = persons[0]["id"]

    # ---------------------------------------------------------
    # Connections
    # ---------------------------------------------------------

    connections = (
        service.get_connections(
            person_id
        )
    )

    print(
        f"\nConnections: "
        f"{len(connections)}"
    )

    for connection in connections:

        print(
            f"\n"
            f"{connection['source_name']}"
            f" --"
            f"{connection['relationship']}"
            f"--> "
            f"{connection['target_name']}"
        )

        if connection["evidence"]:

            print(
                f"Evidence: "
                f"{connection['evidence']}"
            )

    # ---------------------------------------------------------
    # Degree
    # ---------------------------------------------------------

    degree = service.get_degree(
        person_id
    )

    print(
        f"\nDegree: {degree}"
    )

    service.close()


if __name__ == "__main__":
    main()