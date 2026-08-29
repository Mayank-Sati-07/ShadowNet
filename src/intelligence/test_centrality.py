from src.intelligence.graph_loader import (
    load_person_graph
)

from src.intelligence.centrality import (
    calculate_degree,
    calculate_degree_centrality,
    calculate_betweenness,
    calculate_pagerank,
)


def print_top(title, values, limit=10):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    top = sorted(
        values.items(),
        key=lambda x: x[1],
        reverse=True
    )[:limit]

    for person_id, score in top:

        print(
            f"{person_id:<20} "
            f"{score:.6f}"
        )


def main():

    graph = load_person_graph()

    print()
    print(
        f"Graph: "
        f"{graph.number_of_nodes():,} nodes, "
        f"{graph.number_of_edges():,} edges"
    )

    degree = calculate_degree(
        graph
    )

    degree_centrality = (
        calculate_degree_centrality(
            graph
        )
    )

    betweenness = (
        calculate_betweenness(
            graph
        )
    )

    pagerank = calculate_pagerank(
        graph
    )

    print_top(
        "TOP PEOPLE — DEGREE",
        degree
    )

    print_top(
        "TOP PEOPLE — DEGREE CENTRALITY",
        degree_centrality
    )

    print_top(
        "TOP PEOPLE — BETWEENNESS",
        betweenness
    )

    print_top(
        "TOP PEOPLE — PAGERANK",
        pagerank
    )


if __name__ == "__main__":
    main()