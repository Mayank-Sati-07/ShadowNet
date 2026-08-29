from src.intelligence.graph_loader import (
    load_person_graph
)

from src.intelligence.communities import (
    detect_communities,
    community_sizes,
)


def main():

    graph = load_person_graph()

    partition = detect_communities(
        graph
    )

    sizes = community_sizes(
        partition
    )

    print()
    print("=" * 70)
    print("COMMUNITY DETECTION")
    print("=" * 70)

    print(
        f"Total communities: "
        f"{len(sizes)}"
    )

    print()

    for community_id, size in (
        sizes.most_common()
    ):

        print(
            f"Community "
            f"{community_id:<5} "
            f"{size:>5} people"
        )


if __name__ == "__main__":
    main()