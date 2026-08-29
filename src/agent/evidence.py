class EvidenceAggregator:

    @staticmethod
    def aggregate(state):

        graph = state.get(
            "graph_evidence",
            []
        )

        documents = state.get(
            "document_evidence",
            []
        )

        anomalies = state.get(
            "anomaly_evidence",
            []
        )

        return {

            "graph": graph,

            "documents": documents,

            "anomalies": anomalies,

            "evidence_counts": {

                "graph": len(graph),

                "documents": len(documents),

                "anomalies": len(anomalies)
            }
        }