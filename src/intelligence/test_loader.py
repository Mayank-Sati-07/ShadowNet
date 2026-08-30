from src.intelligence.graph_loader import load_person_graph


def main():

    graph = load_person_graph()

    print()
    print("GRAPH TEST")
    print("=" * 50)

    print(
        "Nodes:",
        graph.number_of_nodes()
    )

    print(
        "Edges:",
        graph.number_of_edges()
    )

    print(
        "Connected components:",
        __import__("networkx").number_connected_components(
            graph
        )
    )

    print()
    print("Sample edges:")

    for source, target, data in list(
        graph.edges(data=True)
    )[:10]:

        print(
            source,
            "--",
            target,
            "weight=",
            data["weight"]
        )


if __name__ == "__main__":
    main()