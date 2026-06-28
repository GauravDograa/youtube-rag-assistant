"""
embeddings.py

Responsible for:
1. Loading HuggingFace embedding model
2. Returning a singleton embedding object
"""

from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:

    _embedding = None

    @classmethod
    def get_embedding_model(cls):
        """
        Returns a singleton embedding model.
        Loads only once during the application's lifetime.
        """

        if cls._embedding is None:

            print("Loading embedding model...")

            cls._embedding = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={
                    "device": "cpu"
                },
                encode_kwargs={
                    "normalize_embeddings": True
                }
            )

            print("Embedding model loaded.")

        return cls._embedding