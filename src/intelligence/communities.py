import community.community_louvain as community_louvain
from collections import Counter


def detect_communities(graph):

    partition = community_louvain.best_partition(
        graph,
        weight="weight"
    )

    return partition


def community_sizes(partition):

    return Counter(
        partition.values()
    )