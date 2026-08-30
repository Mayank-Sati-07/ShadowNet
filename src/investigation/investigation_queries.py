# ============================================================
# ShadowNet INVESTIGATION ENGINE
# Reusable Neo4j Cypher queries
# ============================================================


# ------------------------------------------------------------
# 1. Person existence
# ------------------------------------------------------------

PERSON_EXISTS = """
MATCH (p:Person {person_id: $person_id})
RETURN p
LIMIT 1
"""


# ------------------------------------------------------------
# 2. Person profile
# ------------------------------------------------------------

PERSON_PROFILE = """
MATCH (p:Person {person_id: $person_id})

RETURN
    p.person_id AS person_id,
    properties(p) AS properties
LIMIT 1
"""


# ------------------------------------------------------------
# 3. Direct connections
# ------------------------------------------------------------

DIRECT_CONNECTIONS = """
MATCH (p:Person {person_id: $person_id})-[r]-(x)

RETURN
    type(r) AS relationship_type,
    labels(x) AS target_labels,
    properties(x) AS target_properties,
    properties(r) AS relationship_properties

ORDER BY relationship_type
"""


# ------------------------------------------------------------
# 4. Network statistics
# ------------------------------------------------------------

NETWORK_STATISTICS = """
MATCH (p:Person {person_id: $person_id})

OPTIONAL MATCH (p)-[r]-(x)

WITH
    p,
    count(DISTINCT x) AS direct_connections,
    count(r) AS relationship_count

OPTIONAL MATCH path =
    (p)-[*2..2]-(x)

WITH
    p,
    direct_connections,
    relationship_count,
    count(DISTINCT x) AS two_hop_connections

RETURN
    p.person_id AS person_id,
    direct_connections,
    relationship_count,
    two_hop_connections
"""


# ------------------------------------------------------------
# 5. Connected people
# ------------------------------------------------------------

CONNECTED_PEOPLE = """
MATCH (p:Person {person_id: $person_id})-[r]-(other:Person)

RETURN
    other.person_id AS person_id,
    type(r) AS relationship_type,
    properties(r) AS relationship_properties,
    properties(other) AS properties

ORDER BY other.person_id
"""


# ------------------------------------------------------------
# 6. Two-hop people
# ------------------------------------------------------------

TWO_HOP_PEOPLE = """
MATCH
    (p:Person {person_id: $person_id})
    -[*2..2]-
    (other:Person)

WHERE other.person_id <> $person_id

RETURN DISTINCT
    other.person_id AS person_id,
    properties(other) AS properties
"""


# ------------------------------------------------------------
# 7. Phones
# ------------------------------------------------------------

CONNECTED_PHONES = """
MATCH (p:Person {person_id: $person_id})-[r]-(phone:Phone)

RETURN
    phone.phone_id AS phone_id,
    properties(phone) AS properties,
    type(r) AS relationship_type,
    properties(r) AS relationship_properties
"""


# ------------------------------------------------------------
# 8. Vehicles
# ------------------------------------------------------------

CONNECTED_VEHICLES = """
MATCH (p:Person {person_id: $person_id})-[r]-(vehicle:Vehicle)

RETURN
    vehicle.vehicle_id AS vehicle_id,
    properties(vehicle) AS properties,
    type(r) AS relationship_type,
    properties(r) AS relationship_properties
"""


# ------------------------------------------------------------
# 9. Accounts
# ------------------------------------------------------------

CONNECTED_ACCOUNTS = """
MATCH (p:Person {person_id: $person_id})-[r]-(account:Account)

RETURN
    account.account_id AS account_id,
    properties(account) AS properties,
    type(r) AS relationship_type,
    properties(r) AS relationship_properties
"""


# ------------------------------------------------------------
# 10. Locations
# ------------------------------------------------------------

CONNECTED_LOCATIONS = """
MATCH (p:Person {person_id: $person_id})-[r]-(location:Location)

RETURN
    properties(location) AS properties,
    type(r) AS relationship_type,
    properties(r) AS relationship_properties
"""


# ------------------------------------------------------------
# 11. Organizations
# ------------------------------------------------------------

CONNECTED_ORGANIZATIONS = """
MATCH (p:Person {person_id: $person_id})-[r]-(organization:Organization)

RETURN
    properties(organization) AS properties,
    type(r) AS relationship_type,
    properties(r) AS relationship_properties
"""


# ------------------------------------------------------------
# 12. FIRs
# ------------------------------------------------------------

CONNECTED_FIRS = """
MATCH (p:Person {person_id: $person_id})-[r]-(fir:FIR)

RETURN
    properties(fir) AS properties,
    type(r) AS relationship_type,
    properties(r) AS relationship_properties
"""


# ------------------------------------------------------------
# 13. Transactions
#
# Works when transactions are represented as relationships
# carrying transaction properties.
# ------------------------------------------------------------

TRANSACTIONS = """
MATCH (p:Person {person_id: $person_id})-[r]-(x)

WHERE
    r.amount IS NOT NULL

RETURN
    type(r) AS relationship_type,
    labels(x) AS target_labels,
    properties(x) AS target_properties,
    properties(r) AS transaction_properties

ORDER BY
    r.amount DESC
"""


# ------------------------------------------------------------
# 14. Anomalous transactions
# ------------------------------------------------------------

ANOMALOUS_TRANSACTIONS = """
MATCH (p:Person {person_id: $person_id})-[r]-(x)

WHERE
    r.amount IS NOT NULL
    AND (
        coalesce(r.is_anomaly, false) = true
        OR coalesce(r.anomaly_score, 0) > 0.7
    )

RETURN
    type(r) AS relationship_type,
    labels(x) AS target_labels,
    properties(x) AS target_properties,
    properties(r) AS transaction_properties

ORDER BY
    coalesce(r.anomaly_score, 0) DESC,
    r.amount DESC
"""


# ------------------------------------------------------------
# 15. Community
# ------------------------------------------------------------

COMMUNITY = """
MATCH (p:Person {person_id: $person_id})

OPTIONAL MATCH (member:Person)
WHERE member.community_id = p.community_id

RETURN
    p.community_id AS community_id,
    count(DISTINCT member) AS community_size
"""


# ------------------------------------------------------------
# 16. Important people in same community
# ------------------------------------------------------------

COMMUNITY_PEOPLE = """
MATCH (p:Person {person_id: $person_id})

MATCH (member:Person)
WHERE
    member.community_id = p.community_id
    AND member.person_id <> p.person_id

RETURN
    member.person_id AS person_id,
    member.degree AS degree,
    member.degree_centrality AS degree_centrality,
    member.betweenness AS betweenness,
    member.pagerank AS pagerank,
    member.community_id AS community_id

ORDER BY
    coalesce(member.pagerank, 0) DESC

LIMIT 20
"""


# ------------------------------------------------------------
# 17. Investigation paths
#
# Limited to 3 hops to avoid massive result sets.
# ------------------------------------------------------------

INVESTIGATION_PATHS = """
MATCH path =
    (p:Person {person_id: $person_id})-[*1..3]-(x)

RETURN path

LIMIT $limit
"""

# relationship summary : 

RELATIONSHIP_SUMMARY = """
MATCH (p:Person {person_id: $person_id})-[r]-(x)

RETURN
    type(r) AS relationship_type,
    count(r) AS count

ORDER BY count DESC
"""

# ============================================================
# SHORTEST PATH TO ORGANIZATION
# ============================================================
# --------------------------------------------------------
# Advanced Graph Intelligence
# --------------------------------------------------------

SHORTEST_PATH_TO_ORGANIZATION = """
MATCH (person:Person {person_id: $person_id})
MATCH (organization:Organization)
MATCH path = shortestPath(
    (person)-[*..10]-(organization)
)
RETURN
    organization.organization_id AS organization_id,
    organization.organization_type AS organization_type,
    length(path) AS path_length,
    [node IN nodes(path) |
        CASE
            WHEN node.person_id IS NOT NULL
                THEN node.person_id
            WHEN node.organization_id IS NOT NULL
                THEN node.organization_id
            WHEN node.phone_id IS NOT NULL
                THEN node.phone_id
            WHEN node.account_id IS NOT NULL
                THEN node.account_id
            WHEN node.vehicle_id IS NOT NULL
                THEN node.vehicle_id
            WHEN node.location_id IS NOT NULL
                THEN node.location_id
            WHEN node.fir_id IS NOT NULL
                THEN node.fir_id
            ELSE elementId(node)
        END
    ] AS path_nodes,
    [rel IN relationships(path) | type(rel)] AS relationships
ORDER BY path_length ASC
LIMIT 1
"""

SHORTEST_PATH = """
MATCH (person_a:Person {person_id: $person_a})
MATCH (person_b:Person {person_id: $person_b})
MATCH path = shortestPath((person_a)-[*..10]-(person_b))

RETURN
    [node IN nodes(path) |
        CASE
            WHEN node.person_id IS NOT NULL THEN node.person_id
            WHEN node.organization_id IS NOT NULL THEN node.organization_id
            WHEN node.phone_id IS NOT NULL THEN node.phone_id
            WHEN node.account_id IS NOT NULL THEN node.account_id
            WHEN node.vehicle_id IS NOT NULL THEN node.vehicle_id
            WHEN node.location_id IS NOT NULL THEN node.location_id
            WHEN node.fir_id IS NOT NULL THEN node.fir_id
            ELSE elementId(node)
        END
    ] AS nodes,

    [node IN nodes(path) |
        labels(node)
    ] AS node_labels,

    [rel IN relationships(path) |
        type(rel)
    ] AS relationships,

    length(path) AS distance

LIMIT 1
"""


COMMON_CONNECTIONS = """
MATCH (a:Person {person_id: $person_a})
MATCH (b:Person {person_id: $person_b})

MATCH path = (a)-[r1]-(x)-[r2]-(b)

WHERE a <> b

RETURN
    CASE
        WHEN x.person_id IS NOT NULL THEN x.person_id
        WHEN x.phone_id IS NOT NULL THEN x.phone_id
        WHEN x.vehicle_id IS NOT NULL THEN x.vehicle_id
        WHEN x.location_id IS NOT NULL THEN x.location_id
        WHEN x.organization_id IS NOT NULL THEN x.organization_id
        WHEN x.account_id IS NOT NULL THEN x.account_id
        WHEN x.fir_id IS NOT NULL THEN x.fir_id
        ELSE elementId(x)
    END AS common_entity,

    labels(x) AS entity_labels,

    type(r1) AS relationship_from_a,
    type(r2) AS relationship_to_b
"""

JACCARD_SIMILARITY = """
MATCH (a:Person {person_id: $person_a})
MATCH (b:Person {person_id: $person_b})

OPTIONAL MATCH (a)--(a_neighbor)
WITH a, b, collect(DISTINCT a_neighbor) AS a_neighbors

OPTIONAL MATCH (b)--(b_neighbor)
WITH
    a_neighbors,
    collect(DISTINCT b_neighbor) AS b_neighbors

WITH
    [x IN a_neighbors WHERE x IN b_neighbors] AS intersection,
    a_neighbors,
    b_neighbors

WITH
    size(intersection) AS intersection_size,
    size(a_neighbors) AS a_size,
    size(b_neighbors) AS b_size,
    size(intersection) AS union_intersection_size

RETURN
    intersection_size,
    a_size,
    b_size,
    (a_size + b_size - union_intersection_size) AS union_size,

    CASE
        WHEN (a_size + b_size - union_intersection_size) = 0
        THEN 0.0

        ELSE toFloat(intersection_size)
             /
             (a_size + b_size - union_intersection_size)
    END AS jaccard_score
"""

COMMON_NEIGHBORS = """
MATCH (a:Person {person_id: $person_a})
MATCH (b:Person {person_id: $person_b})

MATCH (a)--(common)--(b)

WHERE common <> a
  AND common <> b

RETURN count(DISTINCT common) AS common_neighbors
"""

ADAMIC_ADAR = """
MATCH (a:Person {person_id: $person_a})
MATCH (b:Person {person_id: $person_b})

MATCH (a)--(common)--(b)

WHERE common <> a
  AND common <> b

WITH DISTINCT common

RETURN
    coalesce(
        sum(
            CASE
                WHEN size([(common)--() | 1]) > 1
                THEN 1.0 / log(toFloat(size([(common)--() | 1])))
                ELSE 0.0
            END
        ),
        0.0
    ) AS adamic_adar
"""

LINK_PREDICTION_CANDIDATES = """
MATCH (target:Person {person_id: $person_id})
MATCH (candidate:Person)

WHERE candidate <> target

AND EXISTS {
    MATCH (target)-[*1..2]-(candidate)
}

RETURN DISTINCT candidate.person_id AS person_id
"""

LINK_PREDICTION_CANDIDATES = """
MATCH (target:Person {person_id: $person_id})
MATCH (target)-[*1..2]-(candidate:Person)

WHERE candidate.person_id IS NOT NULL
  AND candidate.person_id <> $person_id

  // Candidate must NOT already have a direct relationship
  AND NOT (target)-[]-(candidate)

RETURN DISTINCT
    candidate.person_id AS person_id

ORDER BY person_id
LIMIT $limit
"""

VERIFY_CANDIDATE = """
MATCH (a:Person {person_id: $person_a})
MATCH (b:Person {person_id: $person_b})

RETURN EXISTS(
    (a)-[]-(b)
) AS directly_connected
"""