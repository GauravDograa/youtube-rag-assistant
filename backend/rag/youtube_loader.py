"""
youtube_loader.py

Responsible for:
1. Extracting YouTube Video ID
2. Downloading transcript
3. Returning cleaned transcript and metadata
"""

import re
from utils.youtube_utils import YouTubeMetadata
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


class YouTubeTranscriptLoader:
    """
    Loads transcript from a YouTube video.
    """

    def __init__(self):
        self.api = YouTubeTranscriptApi()

    def extract_video_id(self, url_or_id: str) -> str:
        """
        Accepts:
            - Full YouTube URL
            - Short URL
            - Embed URL
            - Raw Video ID

        Returns:
            str: YouTube Video ID
        """

        # Already a video ID
        if len(url_or_id) == 11 and "/" not in url_or_id:
            return url_or_id

        patterns = [
            r"v=([a-zA-Z0-9_-]{11})",
            r"youtu\.be/([a-zA-Z0-9_-]{11})",
            r"embed/([a-zA-Z0-9_-]{11})",
            r"shorts/([a-zA-Z0-9_-]{11})",
        ]

        for pattern in patterns:
            match = re.search(pattern, url_or_id)

            if match:
                return match.group(1)

        raise ValueError("Invalid YouTube URL or Video ID")

    def get_transcript(self, url_or_id: str, language: str = "en"):
        """
        Downloads transcript from YouTube.

        Returns:
            transcript (str)
            metadata (dict)
        """

        video_id = self.extract_video_id(url_or_id)

        try:
            transcript_data = self.api.fetch(
                video_id,
                languages=[language]
            )

        except TranscriptsDisabled:
            raise Exception("This video has transcripts disabled.")

        except NoTranscriptFound:
            raise Exception(f"No '{language}' transcript found.")

        except Exception as e:
            raise Exception(f"Transcript Error: {e}")

        # Preserve transcript segments
        segments = []

        for snippet in transcript_data:
            segments.append(
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration,
                }
            )

        # Plain transcript for RAG
        transcript = " ".join(
            segment["text"]
            for segment in segments
        )

        # -----------------------------
        # Transcript metadata
        # -----------------------------

        metadata = {
            "video_id": video_id,
            "language": language,
            "segments": len(segments),
            "characters": len(transcript),
            "transcript_segments": segments,
        }

        # -----------------------------
        # Fetch YouTube metadata
        # -----------------------------

        try:
            video_metadata = YouTubeMetadata.get_metadata(url_or_id)

            metadata.update(video_metadata)

        except Exception as e:
            print(f"Metadata Error: {e}")

        return transcript, metadata