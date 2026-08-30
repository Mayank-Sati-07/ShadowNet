from pathlib import Path


def load_text(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    if file_path.suffix.lower() != ".txt":
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    return file_path.read_text(encoding="utf-8")


def load_fir_directory(directory: str):
    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(directory_path)

    files = sorted(directory_path.glob("*.txt"))

    documents = []

    for file in files:
        documents.append(
            {
                "file_name": file.name,
                "text": file.read_text(encoding="utf-8"),
            }
        )

    return documents