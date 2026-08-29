class GraphAnalytics:

    def __init__(self, neo4j):

        self.neo4j = neo4j

    def degree(self, person_name):

        query = """
        MATCH (p:Person)
        WHERE toLower(p.name) = toLower($name)

        OPTIONAL MATCH (p)-[r]-()

        RETURN
            p.name AS person,
            count(r) AS degree
        """

        return self.neo4j.execute_query(
            query,
            {
                "name": person_name
            }
        )