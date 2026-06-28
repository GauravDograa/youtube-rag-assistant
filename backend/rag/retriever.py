"""
retriever.py

Responsible for:
1. Loading FAISS
2. Creating Retriever
3. Returning relevant transcript chunks
"""
from rag.vector_store import VectorStore


class TranscriptRetriever:

    def __init__(self, k: int = 8):

        self.vector_store = VectorStore().load()

        self.retriever = self.vector_store.as_retriever(

            search_type="mmr",

            search_kwargs={
                "k": k,
                "fetch_k": 30,
            }

        )

    def retrieve(self, question):

        return self.retriever.invoke(question)