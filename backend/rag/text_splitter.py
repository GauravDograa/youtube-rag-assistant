"""
text_splitter.py

Responsible for:
1. Splitting transcript into chunks
2. Returning LangChain Documents
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class TranscriptSplitter:

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 250,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " ",
                "",
            ],
        )

    def split(self, transcript: str, metadata: dict):
        """
        Parameters
        ----------
        transcript : str

        metadata : dict

        Returns
        -------
        List[Document]
        """

        chunks = self.splitter.split_text(transcript)

        documents = []

        for i, chunk in enumerate(chunks):

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "chunk_id": i + 1,
                        "video_id": metadata["video_id"],
                        "language": metadata["language"],
                    },
                )
            )

        return documents