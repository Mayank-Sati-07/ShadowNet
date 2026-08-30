import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.nlp.schemas import FIRExtraction
from src.config import settings


load_dotenv()


class FIRExtractor:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0,
            api_key=settings.google_api_key
        )

        self.structured_llm = (
            self.llm.with_structured_output(
                FIRExtraction
            )
        )

    def extract(self, text: str) -> FIRExtraction:

        if not text or not text.strip():
            raise ValueError(
                "FIR text is empty"
            )

        print(
            "\n========== TEXT SENT TO LLM =========="
        )
        print(text)
        print(
            "======================================"
        )

        prompt = f"""
You are an intelligence analyst extracting
structured information from a police FIR.

Extract ONLY information explicitly present
in the FIR.

DO NOT invent information.

==================================================
ENTITY TYPES
==================================================

Extract:

1. PERSON
2. LOCATION
3. VEHICLE
4. PHONE
5. ORGANIZATION
6. EVENT

==================================================
RELATIONSHIPS
==================================================

Extract relationships explicitly supported
by the FIR.

Allowed relationship types:

MET
COMMUNICATED_WITH
TRAVELLED_TO
USED_VEHICLE
HAS_PHONE
ASSOCIATED_WITH

==================================================
RELATIONSHIP RULES
==================================================

Person meeting person:

Raj Kumar met Amit Sharma

must become:

source = Raj Kumar
relation = MET
target = Amit Sharma

Communication:

Raj Kumar communicated with Amit Sharma

must become:

source = Raj Kumar
relation = COMMUNICATED_WITH
target = Amit Sharma

Travel:

Raj Kumar travelled to Delhi

must become:

source = Raj Kumar
relation = TRAVELLED_TO
target = Delhi

Vehicle:

Raj Kumar used vehicle DL01AB1234

must become:

source = Raj Kumar
relation = USED_VEHICLE
target = DL01AB1234

Phone:

Raj Kumar used phone number 9876543210

must become:

source = Raj Kumar
relation = HAS_PHONE
target = 9876543210

Organization:

Amit Sharma is associated with ABC Logistics

must become:

source = Amit Sharma
relation = ASSOCIATED_WITH
target = ABC Logistics

==================================================
STRICT RULES
==================================================

1. Do not invent entities.
2. Do not infer relationships that are not supported.
3. Preserve entity names exactly.
4. Extract every explicitly mentioned person.
5. Extract every explicitly mentioned location.
6. Extract every explicitly mentioned vehicle.
7. Extract every explicitly mentioned phone.
8. Extract every explicitly mentioned organization.
9. Extract every explicitly mentioned event.
10. Extract relationships supported by the text.
11. Every relationship source MUST exist in the
    extracted entities.
12. Every relationship target MUST exist in the
    extracted entities.
13. Use only the allowed relationship types.
14. Include evidence whenever possible.
15. Preserve dates exactly as written.
16. If the FIR ID is explicitly present, extract it.
17. If there is no FIR ID, return UNKNOWN.

==================================================
FIR DOCUMENT
==================================================

{text}
"""

        print("\n[LLM] Sending extraction request...")

        result = self.structured_llm.invoke(
            prompt
        )

        if result is None:
            raise RuntimeError(
                "LLM returned None"
            )

        print(
            "[LLM] Structured extraction received"
        )

        return result