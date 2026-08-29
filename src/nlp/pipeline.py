import hashlib

from src.nlp.text_extractor import TextExtractor
from src.nlp.entity_extractor import FIRExtractor
from src.nlp.neo4j_writer import FIRNeo4jWriter

from src.nlp.validator import FIRExtractionValidator


class CNASFIRPipeline:

    def __init__(self):

        self.extractor = FIRExtractor()
        self.writer = FIRNeo4jWriter()

    # =========================================================
    # ID GENERATORS
    # =========================================================

    @staticmethod
    def _hash_id(prefix: str, value: str) -> str:

        normalized = value.strip().lower()

        digest = hashlib.sha1(
            normalized.encode("utf-8")
        ).hexdigest()[:10]

        return f"{prefix}_{digest}"

    @classmethod
    def generate_person_id(cls, name):
        return cls._hash_id("NLP_P", name)

    @classmethod
    def generate_location_id(cls, name):
        return cls._hash_id("NLP_L", name)

    @classmethod
    def generate_organization_id(cls, name):
        return cls._hash_id("NLP_O", name)

    @classmethod
    def generate_vehicle_id(cls, registration):
        return cls._hash_id("NLP_V", registration)

    @classmethod
    def generate_phone_id(cls, number):
        return cls._hash_id("NLP_PH", number)

    @staticmethod
    def generate_event_id(
        fir_id,
        event_type,
        date
    ):

        raw = f"{fir_id}:{event_type}:{date}"

        digest = hashlib.sha1(
            raw.encode("utf-8")
        ).hexdigest()[:10]

        return f"NLP_E_{digest}"

    # =========================================================
    # PROCESS
    # =========================================================

    def process(self, document_path):

        print("=" * 70)
        print("CNAS NLP FIR PIPELINE")
        print("=" * 70)

        # =====================================================
        # 1. TEXT EXTRACTION
        # =====================================================

        print("\n[1] Extracting text...")

        text = TextExtractor.extract(
            document_path
        )

        print(
            f"✓ Extracted {len(text):,} characters"
        )

        # =====================================================
        # 2. LLM EXTRACTION
        # =====================================================

        print("\n[2] Extracting entities...")

        extraction = self.extractor.extract(text)

        print("\n[2.5] Validating extraction...")

        FIRExtractionValidator.validate(
            extraction
        )

        print("✓ Extraction validation passed")

        print(
            "✓ Structured extraction completed"
        )

        # =====================================================
        # 3. SUMMARY
        # =====================================================

        print("\n[3] EXTRACTED INFORMATION")

        print(f"Persons: {len(extraction.persons)}")
        print(f"Locations: {len(extraction.locations)}")
        print(f"Organizations: {len(extraction.organizations)}")
        print(f"Vehicles: {len(extraction.vehicles)}")
        print(f"Phones: {len(extraction.phones)}")
        print(f"Events: {len(extraction.events)}")
        print(f"Relationships: {len(extraction.relationships)}")

        # =====================================================
        # 4. CREATE FIR
        # =====================================================

        print("\n[4] Creating FIR...")

        fir_id = extraction.fir_id

        self.writer.create_fir(
            fir_id
        )

        print(
            f"✓ FIR created: {fir_id}"
        )

        # =====================================================
        # ENTITY REGISTRY
        # =====================================================

        entity_registry = {}

        # =====================================================
        # 5. PERSONS
        # =====================================================

        print("\n[5] Writing persons...")

        for person in extraction.persons:

            name = person.name.strip()

            person_id = self.generate_person_id(
                name
            )

            self.writer.create_person(
                person_id,
                name
            )

            self.writer.create_fir_entity_relationship(
                fir_id,
                person_id,
                "Person"
            )

            entity_registry[name] = (
                "Person",
                person_id
            )

        print(
            f"✓ Persons written: {len(extraction.persons)}"
        )

        # =====================================================
        # 6. LOCATIONS
        # =====================================================

        print("\n[6] Writing locations...")

        for location in extraction.locations:

            name = location.name.strip()

            location_id = self.generate_location_id(
                name
            )

            self.writer.create_location(
                location_id,
                name,
                location.location_type
            )

            self.writer.create_fir_entity_relationship(
                fir_id,
                location_id,
                "Location"
            )

            entity_registry[name] = (
                "Location",
                location_id
            )

        print(
            f"✓ Locations written: {len(extraction.locations)}"
        )

        # =====================================================
        # 7. ORGANIZATIONS
        # =====================================================

        print("\n[7] Writing organizations...")

        for organization in extraction.organizations:

            name = organization.name.strip()

            organization_id = (
                self.generate_organization_id(
                    name
                )
            )

            self.writer.create_organization(
                organization_id,
                name
            )

            self.writer.create_fir_entity_relationship(
                fir_id,
                organization_id,
                "Organization"
            )

            entity_registry[name] = (
                "Organization",
                organization_id
            )

        print(
            f"✓ Organizations written: "
            f"{len(extraction.organizations)}"
        )

        # =====================================================
        # 8. VEHICLES
        # =====================================================

        print("\n[8] Writing vehicles...")

        for vehicle in extraction.vehicles:

            registration = (
                vehicle.registration_number.strip()
            )

            vehicle_id = self.generate_vehicle_id(
                registration
            )

            self.writer.create_vehicle(
                vehicle_id,
                registration
            )

            self.writer.create_fir_entity_relationship(
                fir_id,
                vehicle_id,
                "Vehicle"
            )

            entity_registry[registration] = (
                "Vehicle",
                vehicle_id
            )

        print(
            f"✓ Vehicles written: "
            f"{len(extraction.vehicles)}"
        )

        # =====================================================
        # 9. PHONES
        # =====================================================

        print("\n[9] Writing phones...")

        for phone in extraction.phones:

            number = phone.number.strip()

            phone_id = self.generate_phone_id(
                number
            )

            self.writer.create_phone(
                phone_id,
                number
            )

            self.writer.create_fir_entity_relationship(
                fir_id,
                phone_id,
                "Phone"
            )

            entity_registry[number] = (
                "Phone",
                phone_id
            )

        print(
            f"✓ Phones written: "
            f"{len(extraction.phones)}"
        )
        # =====================================================
        # 10. EVENTS
        # =====================================================

        print("\n[10] Writing events...")

        event_count = 0

        for event in extraction.events:

            event_id = self.generate_event_id(
                fir_id,
                event.event_type,
                event.date
            )

            self.writer.create_event(
                event_id,
                event.event_type,
                event.date
            )

            self.writer.create_fir_entity_relationship(
                fir_id,
                event_id,
                "Event"
            )

            # Register event
            entity_registry[
                event.event_type.strip()
            ] = (
                "Event",
                event_id
            )

            event_count += 1

        print(
            f"✓ Events written: {event_count}"
        )

       # =========================================================
        # 11. ENTITY RELATIONSHIPS
        # =========================================================

        print("\n[11] Writing relationships...")

        relationship_count = 0
        relationships_skipped = 0

        for relationship in extraction.relationships:

            source_name = relationship.source.strip()
            target_name = relationship.target.strip()

            source_info = entity_registry.get(source_name)
            target_info = entity_registry.get(target_name)

            if not source_info or not target_info:

                print(
                    f"⚠ Skipping relationship: "
                    f"{source_name} "
                    f"--{relationship.relation}--> "
                    f"{target_name}"
                )

                relationships_skipped += 1
                continue

            source_label, source_id = source_info
            target_label, target_id = target_info

            self.writer.create_relationship(
                source_id=source_id,
                source_label=source_label,
                target_id=target_id,
                target_label=target_label,
                relation=relationship.relation,
                date=relationship.date,
                evidence=relationship.evidence,
            )

            relationship_count += 1

        print(
            f"✓ Relationships written: "
            f"{relationship_count}"
        )

        print(
            f"⚠ Relationships skipped: "
            f"{relationships_skipped}"
        )


        # =====================================================
        # FINAL
        # =====================================================

        print("\n" + "=" * 70)
        print("M8 PIPELINE COMPLETED")
        print("=" * 70)

        return extraction

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        self.writer.close()