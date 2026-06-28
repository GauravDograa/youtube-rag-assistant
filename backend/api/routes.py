"""
routes.py

FastAPI routes for YouTube RAG.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from rag.youtube_loader import YouTubeTranscriptLoader
from rag.text_splitter import TranscriptSplitter
from rag.vector_store import VectorStore
from rag.chain import YouTubeRAG


router = APIRouter()


# -----------------------------
# Initialize components once
# -----------------------------

loader = YouTubeTranscriptLoader()
splitter = TranscriptSplitter()
vector_db = VectorStore()
rag = YouTubeRAG()


# -----------------------------
# Global State
# -----------------------------

FULL_TRANSCRIPT = ""
CURRENT_METADATA = {}


# -----------------------------
# Request Models
# -----------------------------

class VideoRequest(BaseModel):
    url: str


class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Load Video
# -----------------------------

@router.post("/load-video")
def load_video(request: VideoRequest):

    global FULL_TRANSCRIPT
    global CURRENT_METADATA

    transcript, metadata = loader.get_transcript(request.url)
    print("=" * 80)
    print(metadata)
    print("=" * 80)
    FULL_TRANSCRIPT = transcript
    CURRENT_METADATA = metadata

    documents = splitter.split(
        transcript,
        metadata,
    )

    vector_store = vector_db.create(documents)

    vector_db.save(vector_store)

    return {
        "status": "success",
        "message": "Video indexed successfully.",
        "video_id": metadata.get("video_id"),
        "title": metadata.get("title"),
        "channel": metadata.get("channel"),
        "chunks": len(documents),
    }


# -----------------------------
# Ask Question
# -----------------------------

@router.post("/ask")
def ask_question(request: QuestionRequest):

    global FULL_TRANSCRIPT
    global CURRENT_METADATA

    answer = rag.ask(
        question=request.question,
        transcript=FULL_TRANSCRIPT,
        metadata=CURRENT_METADATA,
    )

    return {
        "question": request.question,
        "answer": answer,
    }