import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def main():
    print("=" * 70)
    print("GEMINI CONNECTION TEST")
    print("=" * 70)

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
    )

    response = llm.invoke(
        "Return exactly this sentence: CNAS Gemini test successful."
    )

    print("\nResponse:")
    print(response.content)

    print("\n✓ Gemini connection successful")


if __name__ == "__main__":
    main()
