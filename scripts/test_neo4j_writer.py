from src.nlp.neo4j_writer import FIRNeo4jWriter


def main():

    print("=" * 70)
    print("NEO4J WRITER TEST")
    print("=" * 70)

    writer = FIRNeo4jWriter()

    try:

        print("\n[1] Creating test nodes...")

        writer.create_fir(
            "TEST-FIR-001"
        )

        writer.create_person(
            "TEST-P-001",
            "Test Person A"
        )

        writer.create_person(
            "TEST-P-002",
            "Test Person B"
        )

        print("✓ Nodes created")

        print("\n[2] Creating MENTIONS relationship...")

        writer.create_fir_entity_relationship(
            "TEST-FIR-001",
            "TEST-P-001",
            "Person"
        )

        print("✓ MENTIONS created")

        print("\n[3] Creating entity relationship...")

        writer.create_relationship(
            source_id="TEST-P-001",
            source_label="Person",
            target_id="TEST-P-002",
            target_label="Person",
            relation="MET",
            date="12 August 2026",
            evidence="Test Person A met Test Person B."
        )

        print("✓ MET relationship created")

        print("\n✓ WRITER TEST PASSED")

    finally:

        writer.close()


if __name__ == "__main__":
    main()