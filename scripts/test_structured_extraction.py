import json

from src.nlp.pipeline import FIRPipeline


def main():

    print("=" * 70)
    print("CNAS STRUCTURED FIR EXTRACTION TEST")
    print("=" * 70)

    pipeline = FIRPipeline()

    result = pipeline.process(
        "data/documents/sample_fir.txt"
    )

    print("\n" + "-" * 70)
    print("STRUCTURED EXTRACTION RESULT")
    print("-" * 70)

    print(
        json.dumps(
            result.model_dump(),
            indent=2,
            ensure_ascii=False
        )
    )

    print("\n" + "-" * 70)
    print("VALIDATION")
    print("-" * 70)

    print("✓ Pydantic validation successful")
    print(f"✓ FIR: {result.fir_id}")
    print(f"✓ Persons: {len(result.persons)}")
    print(f"✓ Locations: {len(result.locations)}")
    print(f"✓ Vehicles: {len(result.vehicles)}")
    print(f"✓ Phones: {len(result.phones)}")
    print(f"✓ Organizations: {len(result.organizations)}")
    print(f"✓ Events: {len(result.events)}")
    print(f"✓ Relationships: {len(result.relationships)}")


if __name__ == "__main__":
    main()
