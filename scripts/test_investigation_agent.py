from src.agent.investigation_agent import (
    CNASInvestigationAgent
)


def main():

    print("=" * 70)
    print("CNAS INVESTIGATION AGENT")
    print("=" * 70)

    agent = CNASInvestigationAgent()

    question = (
        "What connections exist between "
        "Raj Kumar and ABC Logistics?"
    )

    print(
        "\nINVESTIGATOR:"
    )

    print(
        question
    )

    result = agent.investigate(
        question
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "INVESTIGATION RESULT"
    )

    print(
        "=" * 70
    )

    print(
        result["final_answer"]
    )


if __name__ == "__main__":
    main()

