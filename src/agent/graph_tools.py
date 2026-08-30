from src.graph.neo4j_client import Neo4jClient


class ShadowNetGraphTools:

    def __init__(self):

        self.client = Neo4jClient()




    # ========================================================
    # FIND PERSON
    # ========================================================

    def find_person(
        self,
        person_name: str
    ):

        query = """
        MATCH (p:Person)
        WHERE toLower(p.name) = toLower($name)

        OPTIONAL MATCH (p)-[r]-(n)

        RETURN
            p.id AS person_id,
            p.name AS name,
            count(r) AS degree,
            collect({
                relation: type(r),
                node_id: n.id,
                node_name: coalesce(
                    n.name,
                    n.number,
                    n.registration_number,
                    n.id
                ),
                node_type: labels(n)
            }) AS connections
        """

        records = self.client.execute_read(
            query,
            {
                "name": person_name
            }
        )

        return records

    # ========================================================
    # PERSON -> ORGANIZATION
    # ========================================================

    def person_organization_connections(
        self,
        person_name: str,
        organization_name: str
    ):

        query = """
        MATCH path =
            (p:Person)-[*1..4]-(o:Organization)

        WHERE
            toLower(p.name) =
            toLower($person_name)

            AND

            toLower(o.name) =
            toLower($organization_name)

        RETURN path
        LIMIT 20
        """

        return self.client.execute_read(
            query,
            {
                "person_name": person_name,
                "organization_name":
                    organization_name
            }
        )

    # ========================================================
    # FIR EVIDENCE
    # ========================================================

    def person_firs(
        self,
        person_name: str
    ):

        query = """
        MATCH (p:Person)<-[:MENTIONS]-(f:FIR)

        WHERE toLower(p.name) =
              toLower($name)

        RETURN
            f.id AS fir_id
        ORDER BY fir_id
        """

        return self.client.execute_read(
            query,
            {
                "name": person_name
            }
        )


    def find_path(
    self,
    source_name: str,
    target_name: str,
    max_hops: int = 5
    ):

        query = f"""
        MATCH (a)
        WHERE toLower(a.name) = toLower($source)

        MATCH (b)
        WHERE toLower(b.name) = toLower($target)

        MATCH p = shortestPath(
            (a)-[*..{max_hops}]-(b)
        )

        RETURN
            [n IN nodes(p) | {{
                name: n.name,
                labels: labels(n)
            }}] AS nodes,

            [r IN relationships(p) | {{
                type: type(r)
            }}] AS relationships

        LIMIT 10
        """

        return self.neo4j.execute_query(
            query,
            {
                "source": source_name,
                "target": target_name
            }
        )

    def close(self):

        self.client.close()

