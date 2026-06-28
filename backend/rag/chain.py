"""
chain.py

Complete YouTube RAG Pipeline
"""

from langchain_core.output_parsers import StrOutputParser

from rag.prompt import RAG_PROMPT
from rag.retriever import TranscriptRetriever
from rag.llm import LocalLLM


SUMMARY_KEYWORDS = [
    "summary",
    "summarize",
    "about",
    "overview",
    "video about",
    "explain the video",
    "gist",
    "main idea",
]

# Questions answered directly from metadata
METADATA_FIELDS = {
    "channel": ["channel", "youtube channel", "channel name"],
    "title": ["title", "video title"],
    "uploader": ["uploader", "uploaded by", "creator"],
    "duration": ["duration", "length", "how long"],
    "upload_date": ["upload date", "published", "when uploaded"],
    "view_count": ["views", "view count"],
}


class YouTubeRAG:

    def __init__(self):

        self.retriever = TranscriptRetriever(k=8)

        self.llm = LocalLLM.get_llm()

        self.parser = StrOutputParser()

    def _metadata_answer(self, question, metadata):

        if not metadata:
            return None

        q = question.lower()

        for field, keywords in METADATA_FIELDS.items():

            if any(keyword in q for keyword in keywords):

                value = metadata.get(field)

                if value:
                    return str(value)

        return None

    def ask(
        self,
        question,
        transcript=None,
        metadata=None,
    ):

        # ---------------------------------
        # 1. Metadata Questions
        # ---------------------------------

        metadata_answer = self._metadata_answer(
            question,
            metadata,
        )

        if metadata_answer:

            return metadata_answer

        # ---------------------------------
        # 2. Summary Questions
        # ---------------------------------

        question_lower = question.lower()

        if transcript and any(
            keyword in question_lower
            for keyword in SUMMARY_KEYWORDS
        ):

            context = f"""
Video Title:
{metadata.get('title', '')}

Channel:
{metadata.get('channel', '')}

Description:
{metadata.get('description', '')}

Transcript:

{transcript}
"""

        # ---------------------------------
        # 3. Normal RAG
        # ---------------------------------

        else:

            docs = self.retriever.retrieve(question)

            retrieved_context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

            context = f"""
Video Title:
{metadata.get('title', '')}

Channel:
{metadata.get('channel', '')}

Description:
{metadata.get('description', '')}

Relevant Transcript:

{retrieved_context}
"""

        prompt = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        response = self.llm.invoke(prompt)

        return self.parser.invoke(response)