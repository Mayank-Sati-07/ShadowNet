from typing import TypedDict, List, Dict, Any


class InvestigationState(TypedDict, total=False):

    question: str

    intent: str

    entity_name: str

    source_person: str

    target_person: str

    graph_evidence: List[Dict[str, Any]]

    document_evidence: List[Dict[str, Any]]

    anomaly_evidence: List[Dict[str, Any]]

    investigation_evidence: Dict[str, Any]

    final_answer: str