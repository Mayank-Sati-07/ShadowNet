from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


class FIRChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split(
        self,
        text: str
    ):

        return self.splitter.split_text(
            text
        )