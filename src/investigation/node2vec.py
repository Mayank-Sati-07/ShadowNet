from pathlib import Path

import networkx as nx
from node2vec import Node2Vec

from src.graph.neo4j_client import Neo4jClient


class ShadowNetNode2Vec:

    def __init__(
        self,
        dimensions=128,
        walk_length=30,
        num_walks=200,
        workers=4,
        window=10,
        min_count=1,
        seed=42,
    ):

        self.dimensions = dimensions
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.workers = workers
        self.window = window
        self.min_count = min_count
        self.seed = seed

        self.client = Neo4jClient()

        self.model = None

    # --------------------------------------------------
    # Extract Person graph from Neo4j
    # --------------------------------------------------

    def load_person_graph(self):

        query = """
        MATCH (a:Person)-[]-(b:Person)
        WHERE a.person_id IS NOT NULL
          AND b.person_id IS NOT NULL

        RETURN DISTINCT
            a.person_id AS source,
            b.person_id AS target
        """

        records = self.client.execute_read(query)

        graph = nx.Graph()

        for record in records:

            source = record["source"]
            target = record["target"]

            if source and target and source != target:

                graph.add_edge(source, target)

        print(
            f"[OK] Person graph loaded: "
            f"{graph.number_of_nodes():,} nodes, "
            f"{graph.number_of_edges():,} edges"
        )

        return graph

    # --------------------------------------------------
    # Train Node2Vec
    # --------------------------------------------------

    def train(self, graph):

        print("\nTraining Node2Vec...")

        node2vec = Node2Vec(
                graph,
                dimensions=self.dimensions,
                walk_length=self.walk_length,
                num_walks=self.num_walks,
                workers=self.workers,
                seed=self.seed,
            )

        self.model = node2vec.fit(
                window=self.window,
                min_count=self.min_count,
            )

        print("[OK] Node2Vec training completed")

        return self.model

    # --------------------------------------------------
    # Get embedding
    # --------------------------------------------------

    def get_embedding(self, person_id):

        if self.model is None:

            raise RuntimeError(
                "Node2Vec model has not been trained."
            )

        if person_id not in self.model.wv:

            return None

        return self.model.wv[person_id]

    # --------------------------------------------------
    # Similarity
    # --------------------------------------------------

    def similarity(self, person_a, person_b):

        vector_a = self.get_embedding(person_a)
        vector_b = self.get_embedding(person_b)

        if vector_a is None or vector_b is None:

            return None

        return float(
            self.model.wv.similarity(
                person_a,
                person_b
            )
        )

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------

    def save(self, path="models/node2vec.model"):

        if self.model is None:

            raise RuntimeError(
                "No Node2Vec model to save."
            )

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.model.wv.save(str(path))

        print(
            f"[OK] Node2Vec embeddings saved to {path}"
        )

    # --------------------------------------------------
    # Close
    # --------------------------------------------------

    def close(self):

        self.client.close()