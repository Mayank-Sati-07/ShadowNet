from pathlib import Path

import pandas as pd

from src.graph.neo4j_client import Neo4jClient


PROCESSED_DIR = Path("data/processed")

RELATIONSHIP_FILES = [
    "relationships_calls.csv",
    "relationships_emails.csv",
    "relationships_transactions.csv",
    "relationships_visits.csv",
    "relationships_works_for.csv",
]


def clean_value(value):

    if pd.isna(value):

        return None

    if hasattr(value, "item"):

        try:
            return value.item()

        except Exception:
            pass

    return value


def load_relationship_file(
    client,
    filename
):

    path = PROCESSED_DIR / filename

    if not path.exists():

        print(f"⚠ Missing: {path}")

        return 0

    df = pd.read_csv(path)

    required_columns = [
        "relationship_id",
        "source_id",
        "source_type",
        "relationship",
        "target_id",
        "target_type"
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"{filename} missing columns: {missing}"
        )

    records = []

    for _, row in df.iterrows():

        record = {}

        for column in df.columns:

            record[column] = clean_value(
                row[column]
            )

        records.append(record)

    # We use the source/target node IDs.
    #
    # Relationship type cannot safely be parameterized
    # in Cypher, so we group records by relationship type.

    total = 0

    for relationship_type, group in df.groupby(
        "relationship"
    ):

        rows = []

        for _, row in group.iterrows():

            properties = {}

            for column in df.columns:

                if column in [
                    "relationship_id",
                    "source_id",
                    "source_type",
                    "relationship",
                    "target_id",
                    "target_type"
                ]:
                    continue

                value = clean_value(row[column])

                if value is not None:

                    properties[column] = value

            rows.append({
                "relationship_id": clean_value(
                    row["relationship_id"]
                ),
                "source_id": clean_value(
                    row["source_id"]
                ),
                "target_id": clean_value(
                    row["target_id"]
                ),
                "properties": properties
            })

        query = f"""
        UNWIND $rows AS row

        MATCH (source)
        WHERE
            source.person_id = row.source_id
            OR source.phone_id = row.source_id
            OR source.vehicle_id = row.source_id
            OR source.location_id = row.source_id
            OR source.organization_id = row.source_id
            OR source.account_id = row.source_id
            OR source.fir_id = row.source_id
            OR source.crime_id = row.source_id
            OR source.station_id = row.source_id
            OR source.statute_id = row.source_id

        MATCH (target)
        WHERE
            target.person_id = row.target_id
            OR target.phone_id = row.target_id
            OR target.vehicle_id = row.target_id
            OR target.location_id = row.target_id
            OR target.organization_id = row.target_id
            OR target.account_id = row.target_id
            OR target.fir_id = row.target_id
            OR target.crime_id = row.target_id
            OR target.station_id = row.target_id
            OR target.statute_id = row.target_id

        MERGE (source)-[r:{relationship_type} {{
            relationship_id: row.relationship_id
        }}]->(target)

        SET r += row.properties
        """

        client.execute(
            query,
            {"rows": rows}
        )

        total += len(rows)

        print(
            f"  [OK] {relationship_type}: "
            f"{len(rows):,}"
        )

    print(
        f"[OK] {filename}: {total:,} relationships"
    )

    return total


def load_all_relationships():

    client = Neo4jClient()

    try:

        client.verify_connection()

        total = 0

        for filename in RELATIONSHIP_FILES:

            total += load_relationship_file(
                client,
                filename
            )

        print()
        print(
            f"Total relationships processed: "
            f"{total:,}"
        )

    finally:

        client.close()


if __name__ == "__main__":
    load_all_relationships()
