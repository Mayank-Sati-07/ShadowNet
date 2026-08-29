from src.graph.neo4j_client import Neo4jClient
from src.investigation.link_prediction import LinkPredictionScorer
from src.investigation.investigation_queries import (
    INVESTIGATION_PATHS,
    RELATIONSHIP_SUMMARY,
)

from src.investigation.investigation_indicators import (
    calculate_indicators
)


from src.investigation.investigation_queries import (
    PERSON_EXISTS,
    PERSON_PROFILE,
    DIRECT_CONNECTIONS,
    NETWORK_STATISTICS,
    CONNECTED_PEOPLE,
    TWO_HOP_PEOPLE,
    CONNECTED_PHONES,
    CONNECTED_VEHICLES,
    CONNECTED_ACCOUNTS,
    CONNECTED_LOCATIONS,
    CONNECTED_ORGANIZATIONS,
    CONNECTED_FIRS,
    TRANSACTIONS,
    ANOMALOUS_TRANSACTIONS,
    COMMUNITY,
    COMMUNITY_PEOPLE,
    SHORTEST_PATH_TO_ORGANIZATION,
    SHORTEST_PATH,
    COMMON_CONNECTIONS,
    JACCARD_SIMILARITY,
    ADAMIC_ADAR,
    COMMON_NEIGHBORS,
    LINK_PREDICTION_CANDIDATES,
    VERIFY_CANDIDATE
)
from src.investigation.investigation_utils import clean_records


class InvestigationEngine:
    """
    CNAS Investigation Engine.

    Provides structured intelligence about a person
    from the Neo4j knowledge graph.
    """

    def __init__(self):

        self.client = Neo4jClient()

        self.client.verify_connection()

        self.link_scorer = LinkPredictionScorer()

    # --------------------------------------------------------
    # Generic query executor
    # --------------------------------------------------------

    def _query(self, query, parameters=None):

        records = self.client.execute_read(
            query,
            parameters
        )

        return clean_records(records)

    # --------------------------------------------------------
    # Person existence
    # --------------------------------------------------------

    def person_exists(self, person_id):

        records = self._query(
            PERSON_EXISTS,
            {
                "person_id": person_id
            }
        )

        return len(records) > 0

    # --------------------------------------------------------
    # Profile
    # --------------------------------------------------------

    def get_profile(self, person_id):

        records = self._query(
            PERSON_PROFILE,
            {
                "person_id": person_id
            }
        )

        if not records:
            return None

        return records[0]

    # --------------------------------------------------------
    # Direct connections
    # --------------------------------------------------------

    def get_direct_connections(self, person_id):

        return self._query(
            DIRECT_CONNECTIONS,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Network statistics
    # --------------------------------------------------------

    def get_network_statistics(self, person_id):

        records = self._query(
            NETWORK_STATISTICS,
            {
                "person_id": person_id
            }
        )

        if not records:

            return {
                "direct_connections": 0,
                "relationship_count": 0,
                "two_hop_connections": 0,
            }

        return records[0]

    # --------------------------------------------------------
    # Connected people
    # --------------------------------------------------------

    def get_connected_people(self, person_id):

        return self._query(
            CONNECTED_PEOPLE,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Two-hop people
    # --------------------------------------------------------

    def get_two_hop_people(self, person_id):

        return self._query(
            TWO_HOP_PEOPLE,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Phones
    # --------------------------------------------------------

    def get_phones(self, person_id):

        return self._query(
            CONNECTED_PHONES,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Vehicles
    # --------------------------------------------------------

    def get_vehicles(self, person_id):

        return self._query(
            CONNECTED_VEHICLES,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Accounts
    # --------------------------------------------------------

    def get_accounts(self, person_id):

        return self._query(
            CONNECTED_ACCOUNTS,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Locations
    # --------------------------------------------------------

    def get_locations(self, person_id):

        return self._query(
            CONNECTED_LOCATIONS,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Organizations
    # --------------------------------------------------------

    def get_organizations(self, person_id):

        return self._query(
            CONNECTED_ORGANIZATIONS,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # FIRs
    # --------------------------------------------------------

    def get_firs(self, person_id):

        return self._query(
            CONNECTED_FIRS,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Transactions
    # --------------------------------------------------------

    def get_transactions(self, person_id):

        return self._query(
            TRANSACTIONS,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Anomalous transactions
    # --------------------------------------------------------

    def get_anomalous_transactions(self, person_id):

        return self._query(
            ANOMALOUS_TRANSACTIONS,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Community
    # --------------------------------------------------------

    def get_community(self, person_id):

        records = self._query(
            COMMUNITY,
            {
                "person_id": person_id
            }
        )

        if not records:

            return {
                "community_id": None,
                "community_size": 0,
            }

        return records[0]

    # --------------------------------------------------------
    # Community people
    # --------------------------------------------------------

    def get_community_people(self, person_id):

        return self._query(
            COMMUNITY_PEOPLE,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Investigation paths
    # --------------------------------------------------------

    def get_investigation_paths(
        self,
        person_id,
        limit=500
    ):

        return self._query(
            INVESTIGATION_PATHS,
            {
                "person_id": person_id,
                "limit": limit,
            }
        )
    def get_relationship_summary(
        self,
        person_id
    ):

        return self._query(
            RELATIONSHIP_SUMMARY,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Shortest path to organization
    # --------------------------------------------------------

    def get_shortest_path_to_organization(self, person_id):

        return self._query(
            SHORTEST_PATH_TO_ORGANIZATION,
            {
                "person_id": person_id
            }
        )

    # --------------------------------------------------------
    # Shortest path between two people
    # --------------------------------------------------------

    def get_shortest_path(self, person_a, person_b):

        return self._query(
            SHORTEST_PATH,
            {
                "person_a": person_a,
                "person_b": person_b
            }
        )

    # COMMON CONNECTION : 

    def get_common_connections(
    self,
    person_a,
    person_b
    ):
        return self._query(
            COMMON_CONNECTIONS,
            {
                "person_a": person_a,
                "person_b": person_b
            }
        )

    # JACORD SIMMILARITYY :

    def calculate_jaccard(
    self,
    person_a,
    person_b
    ):

        records = self._query(
            JACCARD_SIMILARITY,
            {
                "person_a": person_a,
                "person_b": person_b
            }
        )

        if not records:

            return {
                "intersection_size": 0,
                "union_size": 0,
                "jaccard_score": 0.0
            }

        return records[0]


    # COMMON NEIGHBOUR 

    def get_common_neighbors(
    self,
    person_a,
    person_b
    ):

        records = self._query(
            COMMON_NEIGHBORS,
            {
                "person_a": person_a,
                "person_b": person_b
            }
        )

        if not records:

            return 0

        return records[0]["common_neighbors"]

    # ADAMIC ADAR

    def calculate_adamic_adar(
    self,
    person_a,
    person_b
    ):

        records = self._query(
            ADAMIC_ADAR,
            {
                "person_a": person_a,
                "person_b": person_b
            }
        )

        if not records:

            return 0.0

        return records[0]["adamic_adar"]

    # COMMON LINK SCORE 

    def calculate_combined_link_score(
    self,
    person_a,
    person_b
    ):
        """
        Calculate combined graph-based link prediction score.

        Combines:
            - Jaccard similarity
            - Adamic-Adar similarity
        """

        jaccard_result = self.calculate_jaccard(
            person_a,
            person_b
        )

        adamic_result = self.calculate_adamic_adar(
            person_a,
            person_b
        )

        if not jaccard_result:
            return None

        if adamic_result is None:
            return None

        # Jaccard returns a dictionary
        jaccard = jaccard_result["jaccard_score"]

        # Adamic-Adar already returns a float
        adamic_adar = adamic_result

        # Simple normalization for prototype
        normalized_adamic = min(
            adamic_adar / 10.0,
            1.0
        )

        # Weighted combined score
        combined_score = (
            0.5 * jaccard
            +
            0.5 * normalized_adamic
        )

        return {
            "person_a": person_a,
            "person_b": person_b,
            "jaccard": jaccard,
            "adamic_adar": adamic_adar,
            "normalized_adamic_adar": normalized_adamic,
            "combined_score": combined_score
        }

    # LINK PRED : 

    def generate_link_prediction_candidates(
    self,
    person_id,
    limit=100
    ):
        """
        Generate potential new connections for a person.

        Candidates are people within 2 hops who do not
        already have a direct relationship with the target.
        """

        records = self.client.execute_read(
            LINK_PREDICTION_CANDIDATES,
            {
                "person_id": person_id,
                "limit": limit,
            }
        )

        candidates = []

        for record in records:

            candidate_id = record["person_id"]

            if candidate_id:

                candidates.append(candidate_id)

        return candidates



    # verify candidate :

    def is_directly_connected(
    self,
    person_a,
    person_b
    ):

        records = self.client.execute_read(
            VERIFY_CANDIDATE,
            {
                "person_a": person_a,
                "person_b": person_b,
            }
        )

        if not records:
            return False

        return bool(
            records[0]["directly_connected"]
        )

    # RANK LINK PRED

    def rank_link_predictions(
    self,
    person_id,
    limit=10
    ):
        """
        Rank candidate people based on
        Jaccard + Adamic-Adar.
        """

        candidates = self.get_link_prediction_candidates(
            person_id
        )

        results = []

        for candidate in candidates:

            candidate_id = candidate["person_id"]

            if candidate_id == person_id:
                continue

            score = self.calculate_combined_link_score(
                person_id,
                candidate_id
            )

            if score is None:
                continue

            results.append(score)

        results.sort(
            key=lambda x: x["combined_score"],
            reverse=True
        )

        return results[:limit]
    # --------------------------------------------------------
    # Complete investigation
    # --------------------------------------------------------

    def investigate(self, person_id):

        # ----------------------------------------------------
        # Validate person
        # ----------------------------------------------------

        if not self.person_exists(person_id):
            return {
                "success": False,
                "person_id": person_id,
                "error": "Person not found in Neo4j",
            }

        # ----------------------------------------------------
        # Gather intelligence
        # ----------------------------------------------------

        profile = self.get_profile(person_id)

        statistics = self.get_network_statistics(person_id)

        direct_connections = self.get_direct_connections(person_id)

        connected_people = self.get_connected_people(person_id)

        two_hop_people = self.get_two_hop_people(person_id)

        phones = self.get_phones(person_id)

        vehicles = self.get_vehicles(person_id)

        accounts = self.get_accounts(person_id)

        locations = self.get_locations(person_id)

        organizations = self.get_organizations(person_id)

        firs = self.get_firs(person_id)

        transactions = self.get_transactions(person_id)

        anomalous_transactions = (
            self.get_anomalous_transactions(person_id)
        )

        community = self.get_community(person_id)

        community_people = (
            self.get_community_people(person_id)
        )

        relationship_summary = (
            self.get_relationship_summary(person_id)
        )

        # ----------------------------------------------------
        # Build structured response
        # ----------------------------------------------------

        result = {
            "success": True,
            "person_id": person_id,

            "profile": profile,

            "network": {
                "direct_connections": statistics.get(
                    "direct_connections", 0
                ),
                "relationship_count": statistics.get(
                    "relationship_count", 0
                ),
                "two_hop_connections": statistics.get(
                    "two_hop_connections", 0
                ),
                "connected_people": connected_people,
                "two_hop_people": two_hop_people,
                "direct": direct_connections,
            },

            "entities": {
                "phones": phones,
                "vehicles": vehicles,
                "accounts": accounts,
                "locations": locations,
                "organizations": organizations,
                "firs": firs,
            },

            "transactions": {
                "total": len(transactions),
                "anomalous_count": len(
                    anomalous_transactions
                ),
                "all": transactions,
                "anomalous": anomalous_transactions,
            },

            "community": {
                "community_id": community.get(
                    "community_id"
                ),
                "community_size": community.get(
                    "community_size", 0
                ),
                "important_people": community_people,
            },

            "relationship_summary": relationship_summary,
        }

        # ----------------------------------------------------
        # Investigation indicators
        # ----------------------------------------------------

        result["indicators"] = calculate_indicators(result)

        return result

    # --------------------------------------------------------
    # Close connection
    # --------------------------------------------------------

    def close(self):
        self.client.close()