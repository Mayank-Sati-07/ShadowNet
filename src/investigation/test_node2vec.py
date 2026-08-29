from src.investigation.node2vec import CNASNode2Vec


def main():

    print("=" * 70)
    print("CNAS NODE2VEC TEST")
    print("=" * 70)

    person_a = "SYN_P_0001"
    person_b = "SYN_P_0002"

    model = CNASNode2Vec(
        dimensions=128,
        walk_length=30,
        num_walks=100,
        workers=4,
        window=10,
    )

    try:

        graph = model.load_person_graph()

        model.train(graph)

        print()
        print(f"Person A: {person_a}")
        print(f"Person B: {person_b}")

        embedding_a = model.get_embedding(person_a)
        embedding_b = model.get_embedding(person_b)

        if embedding_a is None:

            print(f"⚠ {person_a} not found in embedding")

            return

        if embedding_b is None:

            print(f"⚠ {person_b} not found in embedding")

            return

        print(
            f"\nEmbedding dimension: "
            f"{len(embedding_a)}"
        )

        print(
            "\nPerson A embedding:"
        )

        print(embedding_a[:10])

        print(
            "\nPerson B embedding:"
        )

        print(embedding_b[:10])

        similarity = model.similarity(
            person_a,
            person_b
        )

        print(
            f"\nNode2Vec similarity: "
            f"{similarity:.4f}"
        )

        model.save()

    finally:

        model.close()


if __name__ == "__main__":
    main()