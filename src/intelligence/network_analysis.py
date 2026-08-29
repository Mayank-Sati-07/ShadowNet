import networkx as nx

from src.intelligence.graph_loader import load_person_graph
from src.intelligence.communities import detect_communities


def analyze_graph():

    graph = load_person_graph()

    print(
        f"Graph: {graph.number_of_nodes():,} nodes, "
        f"{graph.number_of_edges():,} edges"
    )

    print("\nCalculating degree...")

    degree = dict(graph.degree())

    print("✓ Degree calculated")

    print("\nCalculating betweenness...")

    betweenness = nx.betweenness_centrality(
        graph,
        normalized=True
    )

    print("✓ Betweenness calculated")

    print("\nCalculating PageRank...")

    pagerank = nx.pagerank(
        graph,
        weight="weight"
    )

    print("✓ PageRank calculated")

    print("\nDetecting communities...")

    communities = detect_communities(graph)

    print("✓ Communities detected")

    results = []

    for person_id in graph.nodes():

        results.append({
            "person_id": person_id,
            "degree": degree.get(person_id, 0),
            "betweenness": betweenness.get(
                person_id,
                0
            ),
            "pagerank": pagerank.get(
                person_id,
                0
            ),
            "community": communities.get(
                person_id
            )
        })

    return results


def main():

    results = analyze_graph()

    results.sort(
        key=lambda x: x["pagerank"],
        reverse=True
    )

    print()
    print("=" * 80)
    print("TOP NETWORKALLY IMPORTANT PERSONS")
    print("=" * 80)

    for result in results[:20]:

        print(
            f"{result['person_id']} | "
            f"degree={result['degree']} | "
            f"betweenness={result['betweenness']:.6f} | "
            f"pagerank={result['pagerank']:.6f} | "
            f"community={result['community']}"
        )


if __name__ == "__main__":
    main()