from src.nlp.schemas import FIRExtraction


ALLOWED_RELATIONS = {
    "MET",
    "COMMUNICATED_WITH",
    "TRAVELLED_TO",
    "USED_VEHICLE",
    "HAS_PHONE",
    "ASSOCIATED_WITH",
}


class FIRExtractionValidator:

    @staticmethod
    def validate(
        extraction: FIRExtraction
    ):

        entities = set()

        for person in extraction.persons:
            entities.add(
                person.name.strip()
            )

        for location in extraction.locations:
            entities.add(
                location.name.strip()
            )

        for vehicle in extraction.vehicles:
            entities.add(
                vehicle.registration_number.strip()
            )

        for phone in extraction.phones:
            entities.add(
                phone.number.strip()
            )

        for organization in extraction.organizations:
            entities.add(
                organization.name.strip()
            )

        for relationship in extraction.relationships:

            if relationship.relation not in ALLOWED_RELATIONS:

                raise ValueError(
                    f"Invalid relationship: "
                    f"{relationship.relation}"
                )

            source = relationship.source.strip()
            target = relationship.target.strip()

            if source not in entities:

                raise ValueError(
                    f"Relationship source not found: "
                    f"{source}"
                )

            if target not in entities:

                raise ValueError(
                    f"Relationship target not found: "
                    f"{target}"
                )

        return True