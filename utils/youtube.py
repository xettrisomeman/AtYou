import os
from googleapiclient.discovery import build

import json
import isodate
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

max_results = 10

# Search for videos


def get_video(query: str, youtube=youtube):
    """
    PARAMETERS
    =========

    query: search query

    youtube: youtube with build version, and developerkey.

    """
    response = (
        youtube.search()
        .list(part="id,snippet", type="video", q=query, maxResults=max_results)
        .execute()
    )
    videos = []
    # Print the video titles and URL
    for video in response["items"]:
        videos.append(
            {
                "videoId": video["id"]["videoId"],
                "link": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                "thumbnails": video["snippet"]["thumbnails"]["default"]["url"],
                "title": video["snippet"]["title"],
            }
        )
    return videos


def duration(id: str, youtube=youtube):
    """
    PARAMETERS
    ==========
    id: id of a video

    """

    response = youtube.videos().list(part="contentDetails", id=id).execute()
    items = response["items"]
    contentDetails = items[0]["contentDetails"]
    duration = isodate.parse_duration(contentDetails["duration"])
    return duration


def get_duration(videos):
    """
    Args:
        videos (_type_): _description_

    Returns:
        _type_: _description_
    """
    durations = []
    for video in videos:
        durations.append(duration(video["videoId"]))
    return durations


youtube.close()
