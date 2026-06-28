"""
llm.py

Loads the local Ollama model.
"""

from langchain_ollama import ChatOllama


class LocalLLM:

    _llm = None

    @classmethod
    def get_llm(cls):

        if cls._llm is None:

            print("Loading Qwen3...")

            cls._llm = ChatOllama(
                model="qwen3:4b",
                temperature=0,
            )

            print("Qwen3 Ready.")

        return cls._llm