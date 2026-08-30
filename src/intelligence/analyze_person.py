from src.intelligence.centrality import (
    calculate_degree,
    calculate_degree_centrality,
    calculate_betweenness,
    calculate_pagerank,
)

from src.intelligence.communities import (
    detect_communities,
    community_sizes,
)


def analyze_graph(graph):

    print("Calculating degree...")

    degree = calculate_degree(
        graph
    )

    print("Calculating degree centrality...")

    degree_centrality = (
        calculate_degree_centrality(
            graph
        )
    )

    print("Calculating betweenness...")

    betweenness = calculate_betweenness(
        graph
    )

    print("Calculating PageRank...")

    pagerank = calculate_pagerank(
        graph
    )

    print("Detecting communities...")

    communities = detect_communities(
        graph
    )

    sizes = community_sizes(
        communities
    )

    results = {}

    for person_id in graph.nodes():

        community_id = communities.get(
            person_id
        )

        results[person_id] = {

            "person_id":
                person_id,

            "degree":
                degree.get(
                    person_id,
                    0
                ),

            "degree_centrality":
                degree_centrality.get(
                    person_id,
                    0.0
                ),

            "betweenness":
                betweenness.get(
                    person_id,
                    0.0
                ),

            "pagerank":
                pagerank.get(
                    person_id,
                    0.0
                ),

            "community_id":
                community_id,

            "community_size":
                sizes.get(
                    community_id,
                    0
                ),
        }

    return results