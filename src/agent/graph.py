from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from src.agent.state import InvestigationState
from src.agent.tools import InvestigationTools
from src.agent.entity_extractor import EntityExtractor
from src.agent.evidence import EvidenceAggregator


load_dotenv()


def extract_text_from_response(response) -> str:
    """
    Normalize LangChain/Gemini AIMessage content
    into a plain string.
    """

    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []

        for block in content:

            if isinstance(block, str):
                parts.append(block)

            elif isinstance(block, dict):
                text = block.get("text")

                if text:
                    parts.append(text)

        return " ".join(parts).strip()

    return str(content).strip()


class CNASInvestigationAgent:

    def __init__(self):

        # -----------------------------------------------------
        # COMPONENTS
        # -----------------------------------------------------

        self.tools = InvestigationTools()

        self.entity_extractor = EntityExtractor()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0
        )

        self.graph = self._build_graph()

    # =========================================================
    # ROUTER
    # =========================================================

    def route(self, state: InvestigationState):

        question = state["question"].lower()

        graph_keywords = [
            "connection",
            "connected",
            "relationship",
            "relationships",
            "network",
            "linked",
            "link",
            "path",
            "between",
            "associated",
            "association",
            "who is connected",
            "how is",
            "why is",
            "involved with",
            "related to"
        ]

        if any(
            keyword in question
            for keyword in graph_keywords
        ):
            return "graph"

        return "rag"

    # =========================================================
    # GRAPH NODE
    # =========================================================

    def graph_node(self, state: InvestigationState):

        question = state["question"]

        # Always initialize evidence
        state["graph_evidence"] = []
        state["document_evidence"] = []

        # -----------------------------------------------------
        # ENTITY EXTRACTION
        # -----------------------------------------------------

        people = self.entity_extractor.extract_people(
            question
        )

        # -----------------------------------------------------
        # TWO PERSON INVESTIGATION
        # -----------------------------------------------------

        if len(people) >= 2:

            source_person = people[0]
            target_person = people[1]

            state["source_person"] = source_person
            state["target_person"] = target_person

            # =================================================
            # 1. DIRECT GRAPH RELATIONSHIP
            # =================================================

            direct = self.tools.get_direct_relationship(
                source_person,
                target_person
            )

            # =================================================
            # 2. MULTI-HOP / SHORTEST PATH
            # =================================================

            path = self.tools.get_person_relationship(
                source_person,
                target_person
            )

            # =================================================
            # 3. DOCUMENT / RAG EVIDENCE
            # =================================================

            rag_result = self.tools.search_documents(
                question
            )

            document_evidence = rag_result.get(
                "evidence",
                []
            )

            # =================================================
            # 4. STORE GRAPH EVIDENCE
            # =================================================

            state["graph_evidence"] = [

                {
                    "type": "direct_relationship",
                    "data": direct
                },

                {
                    "type": "shortest_path",
                    "data": path
                }

            ]

            # =================================================
            # 5. STORE DOCUMENT EVIDENCE
            # =================================================

            state["document_evidence"] = (
                document_evidence
            )

        # -----------------------------------------------------
        # SINGLE PERSON INVESTIGATION
        # -----------------------------------------------------

        elif len(people) == 1:

            person = people[0]

            state["entity_name"] = person

            # =================================================
            # 1. PERSON CONNECTIONS
            # =================================================

            connections = (
                self.tools.get_person_connections(
                    person
                )
            )

            # =================================================
            # 2. DOCUMENT / RAG EVIDENCE
            # =================================================

            rag_result = self.tools.search_documents(
                question
            )

            document_evidence = rag_result.get(
                "evidence",
                []
            )

            # =================================================
            # 3. STORE GRAPH EVIDENCE
            # =================================================

            state["graph_evidence"] = [

                {
                    "type": "connections",
                    "data": connections
                }

            ]

            # =================================================
            # 4. STORE DOCUMENT EVIDENCE
            # =================================================

            state["document_evidence"] = (
                document_evidence
            )

        # -----------------------------------------------------
        # NO PERSON FOUND
        # -----------------------------------------------------

        else:

            state["graph_evidence"] = [

                {
                    "type": "error",
                    "error": "No person entities detected"
                }

            ]

        return state

    # =========================================================
    # RAG NODE
    # =========================================================

    def rag_node(self, state: InvestigationState):

        result = self.tools.search_documents(
            state["question"]
        )

        state["document_evidence"] = (
            result.get(
                "evidence",
                []
            )
        )

        return state

    # =========================================================
    # EVIDENCE AGGREGATOR
    # =========================================================

    def evidence_node(self, state: InvestigationState):

        # Make sure both evidence sources exist
        if "graph_evidence" not in state:
            state["graph_evidence"] = []

        if "document_evidence" not in state:
            state["document_evidence"] = []

        state["investigation_evidence"] = (
            EvidenceAggregator.aggregate(state)
        )

        return state

    # =========================================================
    # FINAL ANSWER
    # =========================================================

    def answer_node(self, state: InvestigationState):

        evidence = state.get(
            "investigation_evidence",
            {}
        )

        prompt = f"""
You are the CNAS Criminal Network Analysis
investigation assistant.

Your job is to summarize an investigation using
ONLY the supplied evidence.

Do NOT invent facts.

==================================================
INVESTIGATION QUESTION
==================================================

{state["question"]}

==================================================
SOURCE PERSON
==================================================

{state.get("source_person", "")}

==================================================
TARGET PERSON
==================================================

{state.get("target_person", "")}

==================================================
INVESTIGATION EVIDENCE
==================================================

{evidence}

==================================================
RULES
==================================================

1. Use ONLY the supplied evidence.

2. Never invent names, relationships, dates,
   organizations, transactions, FIRs, or events.

3. Clearly distinguish:
   - Direct relationship
   - Multi-hop relationship
   - Document evidence
   - Inference

4. A shortest graph path only shows network
   connectivity. It does NOT prove criminal activity.

5. Do NOT infer guilt, criminal intent, or wrongdoing
   from graph proximity.

6. Mention FIR IDs whenever available.

7. Mention relationship types whenever available.

8. Mention graph paths whenever available.

9. Mention document evidence whenever available.

10. If graph evidence and document evidence disagree,
    explicitly state the discrepancy.

11. If evidence is missing, say that it is unavailable.

12. Do not claim that absence of evidence proves
    absence of a relationship.

13. Keep the response concise and investigator-friendly.

==================================================
REQUIRED OUTPUT
==================================================

## Investigation Summary

Briefly summarize the investigation.

## Important Connections

List the important direct or multi-hop connections.

## Supporting Evidence

Mention:
- Neo4j graph evidence
- FIR/document evidence
- Relationship types
- FIR IDs
- Relevant paths

## Limitations / Uncertainty

Clearly state what cannot be established from
the available evidence.
"""

        response = self.llm.invoke(prompt)

        state["final_answer"] = (
            extract_text_from_response(response)
        )

        return state

    # =========================================================
    # BUILD LANGGRAPH WORKFLOW
    # =========================================================

    def _build_graph(self):

        workflow = StateGraph(
            InvestigationState
        )

        # -----------------------------------------------------
        # NODES
        # -----------------------------------------------------

        workflow.add_node(
            "graph",
            self.graph_node
        )

        workflow.add_node(
            "rag",
            self.rag_node
        )

        workflow.add_node(
            "evidence",
            self.evidence_node
        )

        workflow.add_node(
            "answer",
            self.answer_node
        )

        # -----------------------------------------------------
        # START → ROUTER
        # -----------------------------------------------------

        workflow.add_conditional_edges(
            START,
            self.route,
            {
                "graph": "graph",
                "rag": "rag"
            }
        )

        # -----------------------------------------------------
        # GRAPH → EVIDENCE
        # -----------------------------------------------------

        workflow.add_edge(
            "graph",
            "evidence"
        )

        # -----------------------------------------------------
        # RAG → EVIDENCE
        # -----------------------------------------------------

        workflow.add_edge(
            "rag",
            "evidence"
        )

        # -----------------------------------------------------
        # EVIDENCE → ANSWER
        # -----------------------------------------------------

        workflow.add_edge(
            "evidence",
            "answer"
        )

        # -----------------------------------------------------
        # ANSWER → END
        # -----------------------------------------------------

        workflow.add_edge(
            "answer",
            END
        )

        return workflow.compile()

    # =========================================================
    # ASK
    # =========================================================

    def ask(self, question: str):

        result = self.graph.invoke(
            {
                "question": question
            }
        )

        return result

