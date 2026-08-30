from typing import Any


def clean_value(value: Any) -> Any:
    """
    Convert Neo4j/Python values into JSON-friendly values.
    """

    if value is None:
        return None

    if isinstance(value, dict):
        return {
            str(key): clean_value(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [
            clean_value(item)
            for item in value
        ]

    if hasattr(value, "iso_format"):
        try:
            return value.iso_format()
        except Exception:
            pass

    if hasattr(value, "to_native"):
        try:
            return clean_value(value.to_native())
        except Exception:
            pass

    if hasattr(value, "items"):
        try:
            return {
                str(key): clean_value(val)
                for key, val in value.items()
            }
        except Exception:
            pass

    return value


def clean_records(records):
    """
    Convert Neo4j records into JSON-friendly dictionaries.
    """

    cleaned = []

    for record in records:

        if hasattr(record, "data"):
            data = record.data()

        elif isinstance(record, dict):
            data = record

        else:
            data = dict(record)

        cleaned.append(
            clean_value(data)
        )

    return cleaned