from src.graph.neo4j_client import Neo4jClient

def run_metrics():
    client = Neo4jClient()

    print("Computing degree...")
    client.execute_write(
        """
        MATCH (p:Person)
        OPTIONAL MATCH (p)-[r]-()
        WITH p, count(r) AS degree
        SET p.degree = degree
        """
    )
    
    print("Dropping old graph projection if exists...")
    try:
        client.execute_write("CALL gds.graph.drop('personGraph', false)")
    except Exception as e:
        pass

    print("Creating graph projection...")
    client.execute_write(
        """
        CALL gds.graph.project(
          'personGraph',
          '*',
          '*'
        )
        """
    )

    print("Computing PageRank...")
    client.execute_write(
        """
        CALL gds.pageRank.write(
          'personGraph',
          {
            maxIterations: 20,
            dampingFactor: 0.85,
            writeProperty: 'pagerank'
          }
        )
        """
    )

    print("Computing Betweenness Centrality...")
    client.execute_write(
        """
        CALL gds.betweenness.write(
          'personGraph',
          { writeProperty: 'betweenness' }
        )
        """
    )
    
    print("Setting degree_centrality = degree for now...")
    client.execute_write(
        """
        MATCH (p:Person)
        SET p.degree_centrality = toFloat(p.degree)
        """
    )

    print("Done computing metrics.")

if __name__ == "__main__":
    run_metrics()
