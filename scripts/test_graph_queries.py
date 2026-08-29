from src.graph.graph_queries import GraphQueries


def main():

    graph = GraphQueries()

    print("=" * 70)
    print("CNAS GRAPH QUERY TEST")
    print("=" * 70)

    person_id = "YOUR_PERSON_ID"

    print("\n[1] Person")

    result = graph.get_person(person_id)

    print(result)

    print("\n[2] Connections")

    connections = graph.get_person_connections(
        person_id
    )

    for record in connections:
        print(record)

    graph.close()

    print("\n✓ GRAPH QUERY TEST PASSED")


if __name__ == "__main__":
    main()