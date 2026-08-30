from src.graph.neo4j_client import Neo4jClient


class FIRNeo4jWriter:

    # ============================================================
    # ALLOWED GRAPH VALUES
    # ============================================================

    ALLOWED_LABELS = {
        "Person",
        "Location",
        "Organization",
        "Vehicle",
        "Phone",
        "Event",
        "FIR",
    }

    ALLOWED_RELATIONS = {
        "MET",
        "COMMUNICATED_WITH",
        "TRAVELLED_TO",
        "USED_VEHICLE",
        "HAS_PHONE",
        "ASSOCIATED_WITH",
    }

    # ============================================================
    # INIT
    # ============================================================

    def __init__(self):

        self.client = Neo4jClient()

        self.client.verify_connection()

    # ============================================================
    # PERSON
    # ============================================================

    def create_person(self, person_id, name):

        query = """
        MERGE (p:Person {id: $id})
        SET p.name = $name
        """

        self.client.execute_write(
            query,
            {
                "id": person_id,
                "name": name,
            },
        )

    # ============================================================
    # LOCATION
    # ============================================================

    def create_location(
        self,
        location_id,
        name,
        location_type=None,
    ):

        query = """
        MERGE (l:Location {id: $id})
        SET l.name = $name,
            l.location_type = $location_type
        """

        self.client.execute_write(
            query,
            {
                "id": location_id,
                "name": name,
                "location_type": location_type,
            },
        )

    # ============================================================
    # ORGANIZATION
    # ============================================================

    def create_organization(
        self,
        organization_id,
        name,
    ):

        query = """
        MERGE (o:Organization {id: $id})
        SET o.name = $name
        """

        self.client.execute_write(
            query,
            {
                "id": organization_id,
                "name": name,
            },
        )

    # ============================================================
    # VEHICLE
    # ============================================================

    def create_vehicle(
        self,
        vehicle_id,
        registration_number,
    ):

        query = """
        MERGE (v:Vehicle {id: $id})
        SET v.registration_number = $registration_number
        """

        self.client.execute_write(
            query,
            {
                "id": vehicle_id,
                "registration_number": registration_number,
            },
        )

    # ============================================================
    # PHONE
    # ============================================================

    def create_phone(
        self,
        phone_id,
        number,
    ):

        query = """
        MERGE (p:Phone {id: $id})
        SET p.number = $number
        """

        self.client.execute_write(
            query,
            {
                "id": phone_id,
                "number": number,
            },
        )

    # ============================================================
    # EVENT
    # ============================================================

    def create_event(
        self,
        event_id,
        event_type,
        date=None,
    ):

        query = """
        MERGE (e:Event {id: $id})
        SET e.event_type = $event_type,
            e.date = $date
        """

        self.client.execute_write(
            query,
            {
                "id": event_id,
                "event_type": event_type,
                "date": date,
            },
        )

    # ============================================================
    # FIR
    # ============================================================

    def create_fir(self, fir_id):

        query = """
        MERGE (f:FIR {id: $id})
        """

        self.client.execute_write(
            query,
            {
                "id": fir_id,
            },
        )

    # ============================================================
    # FIR -> ENTITY
    # ============================================================

    def create_fir_entity_relationship(
        self,
        fir_id,
        entity_id,
        entity_label,
        evidence=None,
    ):

        if entity_label not in self.ALLOWED_LABELS:
            raise ValueError(
                f"Invalid entity label: {entity_label}"
            )

        query = f"""
        MATCH (f:FIR {{id: $fir_id}})
        MATCH (e:{entity_label} {{id: $entity_id}})
        MERGE (f)-[r:MENTIONS]->(e)
        SET r.evidence = $evidence
        """

        self.client.execute_write(
            query,
            {
                "fir_id": fir_id,
                "entity_id": entity_id,
                "evidence": evidence,
            },
        )

    # ============================================================
    # ENTITY -> ENTITY RELATIONSHIP
    # ============================================================

    def create_relationship(
        self,
        source_id,
        source_label,
        target_id,
        target_label,
        relation,
        date=None,
        evidence=None,
    ):

        # --------------------------------------------------------
        # Validate source label
        # --------------------------------------------------------

        if source_label not in self.ALLOWED_LABELS:

            raise ValueError(
                f"Invalid source label: {source_label}"
            )

        # --------------------------------------------------------
        # Validate target label
        # --------------------------------------------------------

        if target_label not in self.ALLOWED_LABELS:

            raise ValueError(
                f"Invalid target label: {target_label}"
            )

        # --------------------------------------------------------
        # Validate relationship type
        # --------------------------------------------------------

        if relation not in self.ALLOWED_RELATIONS:

            raise ValueError(
                f"Invalid relationship: {relation}"
            )

        # --------------------------------------------------------
        # Neo4j query
        # --------------------------------------------------------

        query = f"""
        MATCH (a:{source_label} {{id: $source_id}})
        MATCH (b:{target_label} {{id: $target_id}})

        MERGE (a)-[r:{relation}]->(b)

        SET r.date = $date,
            r.evidence = $evidence
        """

        self.client.execute_write(
            query,
            {
                "source_id": source_id,
                "target_id": target_id,
                "date": date,
                "evidence": evidence,
            },
        )

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):

        self.client.close()
