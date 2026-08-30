from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from src.agent.state import InvestigationState
from src.agent.graph_tools import ShadowNetGraphTools
from src.agent.rag_tools import ShadowNetRAGTools
from src.config import settings


class ShadowNetInvestigationAgent:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            api_key=settings.google_api_key
        )

        self.graph = ShadowNetGraphTools()

        self.rag = ShadowNetRAGTools()

        builder = StateGraph(
            InvestigationState
        )

        builder.add_node(
            "graph_search",
            self.graph_search
        )

        builder.add_node(
            "document_search",
            self.document_search
        )

        builder.add_node(
            "answer",
            self.generate_answer
        )

        builder.add_edge(
            START,
            "graph_search"
        )

        builder.add_edge(
            "graph_search",
            "document_search"
        )

        builder.add_edge(
            "document_search",
            "answer"
        )

        builder.add_edge(
            "answer",
            END
        )

        self.app = builder.compile()

    # ========================================================
    # GRAPH
    # ========================================================

    def graph_search(
        self,
        state: InvestigationState
    ):

        question = state[
            "question"
        ]

        # For first M9 version we search
        # broadly through the graph.

        results = []

        if "Raj Kumar" in question:

            results = self.graph.find_person(
                "Raj Kumar"
            )

        return {
            "graph_evidence": results
        }

    # ========================================================
    # DOCUMENT
    # ========================================================

    def document_search(
        self,
        state: InvestigationState
    ):

        question = state[
            "question"
        ]

        results = (
            self.rag.search_fir_evidence(
                query=question,
                top_k=5
            )
        )

        return {
            "document_evidence": results
        }

    # ========================================================
    # ANSWER
    # ========================================================

    def generate_answer(
        self,
        state: InvestigationState
    ):

        question = state[
            "question"
        ]

        graph_evidence = state.get(
            "graph_evidence",
            []
        )

        document_evidence = state.get(
            "document_evidence",
            []
        )

        prompt = f"""
You are ShadowNet, a criminal network
investigation assistant.

Answer ONLY using the evidence
provided below.

Do not invent facts.

Clearly distinguish:
- graph evidence
- document evidence
- inference

Investigation question:

{question}

GRAPH EVIDENCE:

{graph_evidence}

DOCUMENT EVIDENCE:

{document_evidence}

Produce:

1. Investigation summary
2. Graph connections
3. Document evidence
4. Important observations
5. Evidence references

If evidence is insufficient,
say so explicitly.
"""

        response = self.llm.invoke(
            prompt
        )

        return {
            "final_answer":
                response.content
        }

    # ========================================================
    # RUN
    # ========================================================

    def investigate(
        self,
        question: str
    ):

        result = self.app.invoke(
            {
                "question": question
            }
        )

        return result
