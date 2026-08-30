from src.graph.neo4j_client import Neo4jClient


class GraphQueries:

    def __init__(self):
        self.client = Neo4jClient()

    def get_person(self, person_id: str):

        query = """
        MATCH (p:Person {id: $person_id})
        RETURN p
        """

        return self.client.execute_read(
            query,
            {"person_id": person_id}
        )

    def get_person_connections(self, person_id: str):

        query = """
        MATCH (p:Person {id: $person_id})
              -[r]-
              (n)
        RETURN
            p.id AS person_id,
            p.name AS person_name,
            type(r) AS relationship,
            labels(n) AS target_labels,
            n.id AS target_id,
            n.name AS target_name
        """

        return self.client.execute_read(
            query,
            {"person_id": person_id}
        )

    def get_fir_entities(self, fir_id: str):

        query = """
        MATCH (f:FIR {id: $fir_id})
              -[r:MENTIONS]->
              (e)
        RETURN
            labels(e) AS labels,
            e.id AS id,
            e.name AS name,
            type(r) AS relationship
        """

        return self.client.execute_read(
            query,
            {"fir_id": fir_id}
        )

    def get_shortest_path(
        self,
        source_id: str,
        target_id: str
    ):

        query = """
        MATCH (a {id: $source_id}),
              (b {id: $target_id})

        MATCH path = shortestPath(
            (a)-[*..6]-(b)
        )

        RETURN path
        """

        return self.client.execute_read(
            query,
            {
                "source_id": source_id,
                "target_id": target_id
            }
        )

    def close(self):
        self.client.close()