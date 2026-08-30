from src.graph.neo4j_client import Neo4jClient


class GraphIntelligenceService:

    def __init__(self):

        self.neo4j = Neo4jClient()

    # =====================================================
    # DEGREE
    # =====================================================

    def get_degree(self, person_name: str):

        query = """
        MATCH (p:Person)
        WHERE toLower(p.name) = toLower($name)

        RETURN
            p.name AS person,
            COUNT { (p)--() } AS degree
        """

        records = self.neo4j.execute_read(
            query,
            {"name": person_name}
        )

        return [
            dict(record)
            for record in records
        ]

    # =====================================================
    # BETWEENNESS
    # =====================================================

    def get_betweenness(
        self,
        limit: int = 20
    ):

        query = """
        CALL gds.betweenness.stream('cnas_graph')
        YIELD nodeId, score

        WITH
            gds.util.asNode(nodeId) AS node,
            score

        WHERE node:Person

        RETURN
            node.name AS person,
            score

        ORDER BY score DESC

        LIMIT $limit
        """

        records = self.neo4j.execute_read(
            query,
            {"limit": limit}
        )

        return [
            dict(record)
            for record in records
        ]

    # =====================================================
    # COMMUNITY
    # =====================================================

    def get_communities(self):

        query = """
        CALL gds.louvain.stream('cnas_graph')
        YIELD nodeId, communityId

        WITH
            gds.util.asNode(nodeId) AS node,
            communityId

        WHERE node:Person

        RETURN
            node.name AS person,
            communityId

        ORDER BY communityId, person
        """

        records = self.neo4j.execute_read(query)

        return [
            dict(record)
            for record in records
        ]

    def get_person_importance(
    self,
    person_name: str
    ):

        degree_query = """
        MATCH (p:Person)
        WHERE toLower(p.name) = toLower($name)

        RETURN
            p.name AS person,
            COUNT { (p)--() } AS degree
        """

        records = self.neo4j.execute_read(
            degree_query,
            {"name": person_name}
        )

        if not records:
            return {
                "person": person_name,
                "error": "Person not found"
            }

        degree = records[0]["degree"]

        betweenness_query = """
        CALL gds.betweenness.stream('cnas_graph')
        YIELD nodeId, score

        WITH gds.util.asNode(nodeId) AS node, score

        WHERE
            node:Person
            AND toLower(node.name) = toLower($name)

        RETURN score
        """

        records = self.neo4j.execute_read(
            betweenness_query,
            {"name": person_name}
        )

        betweenness = (
            records[0]["score"]
            if records
            else 0.0
        )

        return {
            "person": person_name,
            "degree": degree,
            "betweenness": betweenness
        }