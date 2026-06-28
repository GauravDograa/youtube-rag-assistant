"""
vector_store.py

Responsible for:
1. Creating FAISS index
2. Saving index
3. Loading index
4. Returning retriever-ready vector store
"""

import os

from langchain_community.vectorstores import FAISS

from rag.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.embedding_model = EmbeddingModel.get_embedding_model()

        self.index_path = "vector_db/faiss_index"

    def create(self, documents):
        """
        Create FAISS index from LangChain Documents.
        """

        vector_store = FAISS.from_documents(
            documents,
            self.embedding_model
        )

        return vector_store

    def save(self, vector_store):
        """
        Save FAISS index locally.
        """

        os.makedirs(self.index_path, exist_ok=True)

        vector_store.save_local(self.index_path)

        print("FAISS index saved.")

    def load(self):
        """
        Load previously saved FAISS index.
        """

        vector_store = FAISS.load_local(
            self.index_path,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        print("FAISS index loaded.")

        return vector_store