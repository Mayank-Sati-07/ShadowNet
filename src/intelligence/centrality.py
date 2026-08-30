import networkx as nx


def calculate_degree(graph):

    return dict(
        graph.degree()
    )


def calculate_degree_centrality(graph):

    return nx.degree_centrality(
        graph
    )


def calculate_betweenness_unweighted(graph):

    return nx.betweenness_centrality(
        graph,
        normalized=True,
        weight=None
    )


def calculate_betweenness_weighted(graph):

    return nx.betweenness_centrality(
        graph,
        normalized=True,
        weight="distance"
    )


# Backwards-compatible alias: previous code defined `calculate_betweenness`
# (the last definition used weighted betweenness). Provide the old name for
# callers that import `calculate_betweenness`.
calculate_betweenness = calculate_betweenness_weighted

def calculate_pagerank(graph):

    return nx.pagerank(
        graph,
        weight="weight"
    )