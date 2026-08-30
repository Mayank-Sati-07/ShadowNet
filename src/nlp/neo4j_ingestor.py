from typing import Any

from src.graph.neo4j_client import Neo4jClient


class Neo4jFIRIngestor:

    def __init__(self):
        self.client = Neo4jClient()

    def ingest(self, extraction: Any):
        """
        Ingest validated FIR extraction into Neo4j.
        """

        fir_id = extraction.fir_id

        # --------------------------------------------------
        # 1. FIR
        # --------------------------------------------------

        self.client.execute(
            """
            MERGE (f:FIR {fir_id: $fir_id})
            RETURN f
            """,
            {"fir_id": fir_id}
        )

        # --------------------------------------------------
        # 2. Persons
        # --------------------------------------------------

        for person in extraction.persons:

            self.client.execute(
                """
                MERGE (p:Person {name: $name})
                RETURN p
                """,
                {
                    "name": person.name
                }
            )

            self.client.execute(
                """
                MATCH (f:FIR {fir_id: $fir_id})
                MATCH (p:Person {name: $name})
                MERGE (f)-[:MENTIONS]->(p)
                """,
                {
                    "fir_id": fir_id,
                    "name": person.name
                }
            )

        # --------------------------------------------------
        # 3. Locations
        # --------------------------------------------------

        for location in extraction.locations:

            self.client.execute(
                """
                MERGE (l:Location {name: $name})
                SET l.location_type = $location_type
                RETURN l
                """,
                {
                    "name": location.name,
                    "location_type": location.location_type
                }
            )

            self.client.execute(
                """
                MATCH (f:FIR {fir_id: $fir_id})
                MATCH (l:Location {name: $name})
                MERGE (f)-[:MENTIONS]->(l)
                """,
                {
                    "fir_id": fir_id,
                    "name": location.name
                }
            )

        # --------------------------------------------------
        # 4. Vehicles
        # --------------------------------------------------

        for vehicle in extraction.vehicles:

            self.client.execute(
                """
                MERGE (v:Vehicle {
                    registration_number: $registration_number
                })
                RETURN v
                """,
                {
                    "registration_number":
                        vehicle.registration_number
                }
            )

        # --------------------------------------------------
        # 5. Phones
        # --------------------------------------------------

        for phone in extraction.phones:

            self.client.execute(
                """
                MERGE (p:Phone {number: $number})
                RETURN p
                """,
                {
                    "number": phone.number
                }
            )

        # --------------------------------------------------
        # 6. Organizations
        # --------------------------------------------------

        for organization in extraction.organizations:

            self.client.execute(
                """
                MERGE (o:Organization {name: $name})
                RETURN o
                """,
                {
                    "name": organization.name
                }
            )

        # --------------------------------------------------
        # 7. Relationships
        # --------------------------------------------------

        self._create_relationships(
            extraction.relationships
        )

        print("[OK] Neo4j ingestion completed")

    # ======================================================
    # Relationship creation
    # ======================================================

    def _create_relationships(self, relationships):

        allowed_relationships = {
            "MET",
            "COMMUNICATED_WITH",
            "TRAVELLED_TO",
            "VISITED",
            "LOCATED_AT",
            "USED_VEHICLE",
            "HAS_PHONE",
            "ASSOCIATED_WITH",
            "WORKS_FOR",
        }

        for rel in relationships:

            relation = rel.relation.upper()

            if relation not in allowed_relationships:
                print(
                    f"⚠ Skipping unsupported relationship: "
                    f"{relation}"
                )
                continue

            query = f"""
            MATCH (source {{name: $source}})
            MATCH (target {{name: $target}})
            MERGE (source)-[r:{relation}]->(target)
            SET r.date = $date,
                r.evidence = $evidence
            """

            self.client.execute(
                query,
                {
                    "source": rel.source,
                    "target": rel.target,
                    "date": getattr(
                        rel,
                        "date",
                        None
                    ),
                    "evidence": getattr(
                        rel,
                        "evidence",
                        None
                    ),
                }
            )