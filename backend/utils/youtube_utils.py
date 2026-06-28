"""
youtube_utils.py

Utility functions for fetching YouTube metadata.
"""

import yt_dlp


class YouTubeMetadata:

    @staticmethod
    def get_metadata(url: str):

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title"),
            "channel": info.get("channel"),
            "uploader": info.get("uploader"),
            "description": info.get("description"),
            "duration": info.get("duration"),
            "upload_date": info.get("upload_date"),
            "view_count": info.get("view_count"),
            "thumbnail": info.get("thumbnail"),
            "webpage_url": info.get("webpage_url"),
        }