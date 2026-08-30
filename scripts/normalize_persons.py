from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw/CNAS_Prototype_Data")
OUT_DIR = Path("data/processed")

OUT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_synthetic():

    df = pd.read_csv(
        RAW_DIR / "synthetic_persons.csv"
    )

    result = pd.DataFrame({
        "person_id": df["person_id"],
        "community_id": df["community_id"],
        "source": df["data_provenance"],
        "source_role": df["source_role"],
        "confidence": 1.0
    })

    return result


def normalize_fir():

    df = pd.read_csv(
        RAW_DIR / "source_persons_pseudonymized.csv"
    )

    result = pd.DataFrame({
        "person_id": df["person_id"],
        "community_id": pd.NA,
        "source": df["data_provenance"],
        "source_role": df["source_role"],
        "confidence": df["source_avg_confidence"]
    })

    return result


def main():

    synthetic = normalize_synthetic()
    fir = normalize_fir()

    persons = pd.concat(
        [synthetic, fir],
        ignore_index=True
    )

    # Validate IDs
    persons = persons.drop_duplicates(
        subset=["person_id"]
    )

    persons.to_csv(
        OUT_DIR / "persons.csv",
        index=False
    )

    print(f"Persons created: {len(persons)}")


if __name__ == "__main__":
    main()