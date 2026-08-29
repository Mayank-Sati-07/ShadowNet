import networkx as nx


def calculate_degree(graph):

    return dict(
        graph.degree()
    )


def calculate_degree_centrality(graph):

    return nx.degree_centrality(
        graph
    )


def calculate_betweenness(graph):

    return nx.betweenness_centrality(
        graph,
        normalized=True,
        weight=None
    )


def calculate_betweenness(graph):

    return nx.betweenness_centrality(
        graph,
        normalized=True,
        weight="distance"
    )

def calculate_pagerank(graph):

    return nx.pagerank(
        graph,
        weight="weight"
    )