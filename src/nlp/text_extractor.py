from pathlib import Path
from pypdf import PdfReader


class TextExtractor:

    @staticmethod
    def extract_from_txt(path: str) -> str:

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(path)

        return file_path.read_text(
            encoding="utf-8"
        )

    @staticmethod
    def extract_from_pdf(path: str) -> str:

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(path)

        reader = PdfReader(str(file_path))

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    @classmethod
    def extract(cls, path: str) -> str:

        suffix = Path(path).suffix.lower()

        if suffix == ".txt":
            return cls.extract_from_txt(path)

        if suffix == ".pdf":
            return cls.extract_from_pdf(path)

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )