import re


class EntityNormalizer:

    @staticmethod
    def normalize_name(name: str) -> str:

        name = name.strip().lower()

        name = re.sub(
            r"\s+",
            " ",
            name
        )

        return name

    @staticmethod
    def normalize_phone(number: str) -> str:

        digits = re.sub(
            r"\D",
            "",
            number
        )

        return digits

    @staticmethod
    def normalize_vehicle(
        registration_number: str
    ) -> str:

        value = registration_number.upper()

        value = re.sub(
            r"[^A-Z0-9]",
            "",
            value
        )

        return value