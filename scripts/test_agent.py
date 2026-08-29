from src.agent.graph import (
    CNASInvestigationAgent
)

from dotenv import load_dotenv

load_dotenv()

def main():

    print("=" * 70)
    print("CNAS AI INVESTIGATION AGENT")
    print("=" * 70)

    agent = (
        CNASInvestigationAgent()
    )

    questions = [

        "How is Raj Kumar connected to Amit Sharma?",

        "What evidence mentions Raj Kumar?",

    ]

    for question in questions:

        print("\n" + "=" * 70)

        print(
            f"QUESTION:\n{question}"
        )

        result = agent.ask(
            question
        )

        print(
            "\nANSWER:"
        )

        print(
            result["final_answer"]
        )


if __name__ == "__main__":
    main()