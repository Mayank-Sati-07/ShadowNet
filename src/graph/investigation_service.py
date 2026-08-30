from src.graph.neo4j_client import Neo4jClient


class GraphInvestigationService:

    def __init__(self):

        self.client = Neo4jClient()
        self.neo4j = self.client

        self.client.verify_connection()

    # =========================================================
    # FIND PERSON
    # =========================================================

    def find_paths(
        self,
        source_id: str,
        target_id: str,
        max_hops: int = 4
    ):

        query = f"""
        MATCH (a)
        WHERE
            a.id = $source_id
            OR a.person_id = $source_id

        MATCH (b)
        WHERE
            b.id = $target_id
            OR b.person_id = $target_id

        MATCH path =
            (a)-[*1..{max_hops}]-(b)

        RETURN path

        LIMIT 20
        """

        return self.client.execute_read(
            query,
            {
                "source_id": source_id,
                "target_id": target_id,
            }
        )

    # =========================================================
    # PERSON CONNECTIONS
    # =========================================================
    def get_connections(
        self,
        person_id: str
    ):

        query = """
        MATCH (p:Person)
        WHERE coalesce(p.id, p.person_id) = $person_id

        MATCH (p)-[r]->(n)

        RETURN
            coalesce(p.id, p.person_id) AS source_id,
            p.name AS source_name,
            type(r) AS relationship,
            coalesce(n.id, n.person_id) AS target_id,
            labels(n) AS target_labels,
            coalesce(
                n.name,
                n.registration_number,
                n.number,
                n.event_type,
                n.id,
                n.person_id
            ) AS target_name,
            r.date AS date,
            r.evidence AS evidence
        """

        return self.client.execute_read(
            query,
            {
                "person_id": person_id
            }
        )
    # =========================================================
    # DIRECT RELATIONSHIP
    # =========================================================

    def get_direct_relationship(
        self,
        source_person: str,
        target_person: str
    ):

        query = """
        MATCH (a:Person)
        WHERE
            toLower(a.name) = toLower($source)

        MATCH (b:Person)
        WHERE
            toLower(b.name) = toLower($target)

        MATCH (a)-[r]-(b)

        RETURN
            a.name AS source,
            type(r) AS relationship,
            b.name AS target,
            properties(r) AS relationship_properties
        """

        return self.client.execute_read(
            query,
            {
                "source": source_person,
                "target": target_person
            }
        )

    # =========================================================
    # SHORTEST PATH
    # =========================================================

    def get_person_relationship(
        self,
        source_person: str,
        target_person: str,
        max_hops: int = 5
    ):

        query = f"""
        MATCH (a:Person)
        WHERE toLower(a.name) = toLower($source)

        MATCH (b:Person)
        WHERE toLower(b.name) = toLower($target)

        MATCH p = shortestPath(
            (a)-[*..{max_hops}]-(b)
        )

        RETURN
            a.name AS source,
            b.name AS target,

            [node IN nodes(p) |
                coalesce(node.name,
                         node.person_id,
                         node.id)
            ] AS nodes,

            [rel IN relationships(p) |
                type(rel)
            ] AS relationships

        LIMIT 5
        """

        return self.client.execute_read(
            query,
            {
                "source": source_person,
                "target": target_person
            }
        )

    # =========================================================
    # DEGREE
    # =========================================================

    def get_degree(
        self,
        person_id: str
    ):

        query = """
        MATCH (p:Person)
        WHERE coalesce(p.id, p.person_id) = $person_id

        OPTIONAL MATCH (p)-[r]-()

        RETURN count(r) AS degree
        """

        return self.client.execute_read(
            query,
            {
                "person_id": person_id
            }
        )
    # =========================================================
    # NETWORK INTELLIGENCE
    # =========================================================

    def get_person_intelligence(
        self,
        person_id: str
    ):

        query = """
        MATCH (p:Person)

        WHERE
            coalesce(p.person_id, p.id) = $person_id

        RETURN
            coalesce(p.person_id, p.id) AS person_id,
            p.name AS name,

            p.degree AS degree,
            p.degree_centrality AS degree_centrality,
            p.betweenness AS betweenness,
            p.pagerank AS pagerank,

            p.community_id AS community,
            p.community_size AS community_size
        """

        records = self.client.execute_read(
            query,
            {
                "person_id": person_id
            }
        )

        if not records:
            return {
                "error": f"Person '{person_id}' not found"
            }

        return dict(records[0])

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        self.client.close()