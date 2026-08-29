import sys
import json

from src.investigation.investigation_engine import (
    InvestigationEngine
)


def main():

    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "uv run python -m "
            "src.investigation.run_investigation "
            "SYN_P_0001"
        )

        sys.exit(1)

    person_id = sys.argv[1]

    engine = InvestigationEngine()

    try:

        result = engine.investigate(
            person_id
        )

        print(
            json.dumps(
                result,
                indent=2,
                default=str
            )
        )

    finally:

        engine.close()


if __name__ == "__main__":

    main()