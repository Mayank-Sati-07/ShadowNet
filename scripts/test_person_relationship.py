from src.agent.tools import InvestigationTools


def main():

    tools = InvestigationTools()

    result = tools.get_person_relationship(
        "Raj Kumar",
        "Amit Sharma"
    )

    print("=" * 70)
    print("PERSON RELATIONSHIP TEST")
    print("=" * 70)

    print(result)


if __name__ == "__main__":
    main()