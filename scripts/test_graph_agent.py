from src.agent.graph_tools import CNASGraphTools


def main():

    print("=" * 70)
    print("CNAS GRAPH INVESTIGATION TEST")
    print("=" * 70)

    graph = CNASGraphTools()

    # --------------------------------------------------------
    # PERSON
    # --------------------------------------------------------

    print(
        "\n[1] Finding Raj Kumar..."
    )

    results = graph.find_person(
        "Raj Kumar"
    )

    for record in results:

        print(
            "\nPerson:",
            record["name"]
        )

        print(
            "Degree:",
            record["degree"]
        )

        print(
            "Connections:"
        )

        for connection in record[
            "connections"
        ]:

            print(
                " ",
                connection
            )

    # --------------------------------------------------------
    # PERSON -> ORGANIZATION
    # --------------------------------------------------------

    print(
        "\n[2] Raj Kumar -> ABC Logistics"
    )

    paths = (
        graph.person_organization_connections(
            "Raj Kumar",
            "ABC Logistics"
        )
    )

    print(
        "Paths found:",
        len(paths)
    )

    # --------------------------------------------------------
    # FIR
    # --------------------------------------------------------

    print(
        "\n[3] FIR evidence"
    )

    firs = graph.person_firs(
        "Raj Kumar"
    )

    for fir in firs:

        print(
            "FIR:",
            fir["fir_id"]
        )

    graph.close()


if __name__ == "__main__":
    main()
