from langchain_core.documents import Document

from src.nlp.text_extractor import TextExtractor


class FIRDocumentLoader:

    @staticmethod
    def load(path: str, fir_id: str):

        text = TextExtractor.extract(path)

        return Document(
            page_content=text,
            metadata={
                "fir_id": fir_id,
                "source": path,
                "document_type": "FIR"
            }
        )