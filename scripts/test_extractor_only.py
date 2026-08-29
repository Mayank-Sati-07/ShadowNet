from src.nlp.text_extractor import TextExtractor
from src.nlp.entity_extractor import FIRExtractor


def main():

    path = "data/documents/sample_fir.txt"

    print("=" * 70)
    print("CNAS LLM EXTRACTION TEST")
    print("=" * 70)

    print("\n[1] Reading FIR...")

    text = TextExtractor.extract(path)

    print(
        f"✓ Text extracted: {len(text)} characters"
    )

    print("\n[2] Running LLM extraction...")

    extractor = FIRExtractor()

    result = extractor.extract(text)

    print("\n[3] EXTRACTION RESULT")
    print("=" * 70)

    print(
        result.model_dump_json(
            indent=2
        )
    )

    print("\n[4] COUNTS")
    print("=" * 70)

    print(
        "Persons:",
        len(result.persons)
    )

    print(
        "Locations:",
        len(result.locations)
    )

    print(
        "Organizations:",
        len(result.organizations)
    )

    print(
        "Vehicles:",
        len(result.vehicles)
    )

    print(
        "Phones:",
        len(result.phones)
    )

    print(
        "Events:",
        len(result.events)
    )

    print(
        "Relationships:",
        len(result.relationships)
    )


if __name__ == "__main__":
    main()


