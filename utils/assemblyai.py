import os
import requests
from pytube import YouTube


URL = "https://whisper.lablab.ai/detect_language"


def download_youtube(youtube_url: str):
    """
    Download youtube video based on provided url.

    Args:
        youtube_url (str): youtube video url

    Returns:
        new_file: name of saved file.
        base: title of the video
    """
    yt_ = YouTube(youtube_url)
    title = yt_.title
    thumbnail = yt_.thumbnail_url
    video = yt_.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".")
    base, _ = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    return new_file, title, thumbnail


def detect_language(filename: str):
    """
    Detect language of filename.

    Args:
        filename (str): name of the file

    Returns:
        response.text : returns json data
    """
    url = "https://whisper.lablab.ai/detect-language"
    payload = {}
    files = {"audio_file": (filename, open(filename, "rb"), "audio/wpeg")}
    response = requests.post(url, files=files, params=payload, timeout=80)
    return response.text


def transcribe(filename: str, language):
    """Transcribe youtube video based on provided language and filename

    Args:
        filename (str): name of a file
        language (str): language of wav

    Returns:
        response.text : dict value of transcribed audio
    """

    url = "https://whisper.lablab.ai/asr"
    payload = {"task": "transcribe", "language": language}
    files = {"audio_file": (filename, open(filename, "rb"), "audio/mpeg")}
    response = requests.post(url, files=files, params=payload, timeout=80)
    return response.text
