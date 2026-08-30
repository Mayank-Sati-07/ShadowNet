import json

from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import settings


class EntityExtractor:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            api_key=settings.google_api_key
        )

    def extract_people(self, question: str):

        prompt = f"""
You are an entity extraction system for a criminal investigation platform.

Extract the people mentioned in the question.

Question:
{question}

Return ONLY valid JSON.

Format:

{{
    "people": [
        "Person 1",
        "Person 2"
    ]
}}

Rules:

- Return only actual person names.
- Preserve the names exactly.
- Do not add explanations.
- If only one person exists, return one name.
"""

        response = self.llm.invoke(prompt)

        content = response.content

        if isinstance(content, list):

            parts = []

            for block in content:

                if isinstance(block, str):
                    parts.append(block)

                elif isinstance(block, dict):
                    text = block.get("text")

                    if text:
                        parts.append(text)

            content = "".join(parts)

        content = content.strip()

        # Remove markdown fences if Gemini adds them
        if content.startswith("```"):

            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        try:

            data = json.loads(content)

            return data.get("people", [])

        except json.JSONDecodeError:

            return []