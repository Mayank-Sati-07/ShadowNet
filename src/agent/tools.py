from src.rag.rag_pipeline import FIRRAGPipeline
from src.graph.investigation_service import (
    GraphInvestigationService
)

from src.graph.graph_intelligence import (
    GraphIntelligenceService
)

class InvestigationTools:

    def __init__(self):

        # Do not initialize heavy RAG pipeline at construction time.
        # Instantiate graph services (lightweight) and lazily create RAG when needed.
        self._rag = None

        self.graph = GraphInvestigationService()

        self.graph_intelligence = GraphIntelligenceService()

    @property
    def rag(self):
        if self._rag is None:
            print("[INFO] Initializing RAG pipeline lazily (this should run offline if possible)")
            self._rag = FIRRAGPipeline()
        return self._rag

    # =========================================================
    # RAG
    # =========================================================

    def search_documents(
        self,
        question: str
    ):

        result = self.rag.ask(
            question=question,
            top_k=5
        )

        return result

    # =========================================================
    # GRAPH
    # =========================================================

    def get_person_connections(
        self,
        person_name: str
    ):

        persons = self.graph.find_person(
            person_name
        )

        if not persons:

            return {
                "error": (
                    f"Person '{person_name}' "
                    "not found"
                )
            }

        person_id = persons[0]["id"]

        connections = (
            self.graph.get_connections(
                person_id
            )
        )

        return {
            "person": persons[0],
            "connections": connections
        }

    

    def get_person_relationship(
    self,
    source_person: str,
    target_person: str
    ):

        query = """
        MATCH (a:Person)
        WHERE toLower(a.name) = toLower($source)

        MATCH (b:Person)
        WHERE toLower(b.name) = toLower($target)

        MATCH p = shortestPath(
            (a)-[*..5]-(b)
        )

        RETURN
            a.name AS source,
            b.name AS target,
            [node IN nodes(p) | coalesce(node.name, node.id)] AS nodes,
            [rel IN relationships(p) | type(rel)] AS relationships
        LIMIT 5
        """

        try:

            records = self.graph.neo4j.execute_read(
                query,
                {
                    "source": source_person,
                    "target": target_person
                }
            )

            return {
                "source": source_person,
                "target": target_person,
                "paths": [dict(record) for record in records]
            }

        except Exception as e:

            return {
                "source": source_person,
                "target": target_person,
                "error": str(e)
            }


    def get_direct_relationship(
        self,
        source_person: str,
        target_person: str
    ):

        query = """
        MATCH (a:Person)-[r]-(b:Person)

        WHERE
            toLower(a.name) = toLower($source)
            AND
            toLower(b.name) = toLower($target)

        RETURN
            a.name AS source,
            type(r) AS relationship,
            b.name AS target
        """

        try:

            records = self.graph.neo4j.execute_read(
                query,
                {
                    "source": source_person,
                    "target": target_person
                }
            )

            return [
                dict(record)
                for record in records
            ]

        except Exception as e:

            return {
                "error": str(e)
            }

    def get_person_intelligence(
    self,
    person_name: str
    ):

        return (
            self.graph_intelligence
            .get_person_importance(
                person_name
            )
        )