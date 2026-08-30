from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class FIRAnswerGenerator:

    def __init__(self):

        # Lazy initialize LLM to avoid requiring Google credentials at import
        self._llm = None
        self._temperature = 0

    @property
    def llm(self):
        if self._llm is None:
            print("[INFO] Initializing FIRAnswerGenerator LLM lazily")
            self._llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=self._temperature)
        return self._llm

    def generate(
        self,
        question: str,
        evidence: list[dict]
    ):

        if not evidence:

            return (
                "No relevant FIR evidence "
                "was found."
            )

        evidence_text = "\n\n".join(
            [
                (
                    f"Evidence {i + 1}\n"
                    f"FIR: {item.get('fir_id')}\n"
                    f"Score: {item.get('score'):.4f}\n"
                    f"Text: {item.get('text')}"
                )
                for i, item in enumerate(evidence)
            ]
        )

        prompt = f"""
You are the CNAS investigation assistant.

Answer the investigator's question using
ONLY the supplied evidence.

Do not invent facts.

If the evidence does not establish something,
say that it is not established by the available
evidence.

Clearly distinguish:
- directly stated facts
- reasonable observations
- unavailable information

Investigator question:

{question}

Retrieved evidence:

{evidence_text}

Provide a concise investigation-oriented answer.
"""

        response = self.llm.invoke(prompt)

        return response.content