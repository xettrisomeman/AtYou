"""Helper functions"""

import os
import json


def read_file(file: str):
    """Take file and read it

    Args:
        file (str): filename

    Returns:
        file_str: string
    """
    with open(file, "r", encoding="utf-8") as f:
        file_str = f.read()
    return file_str


def download_vido(download_youtube, detect_language, transcribe, video: str):
    """Takes in video url

    Args:
        download_youtube (function): _a function to download youtube video
        detect_language (function): detect language of the video
        transcribe (function): function that takes audio and returns text
        video (str): url of the video link

    Returns:
        text. title, thumbnail = str, str, str
    """
    file_name, title, thumbnail = download_youtube(video)
    language_code = json.loads(detect_language(file_name))["langauge_code"]
    text = json.loads(transcribe(file_name, language_code))["text"]
    os.remove(file_name)
    return text, title, thumbnail


def check_tokens(text_len):
    """Check tokens

    Args:
        text_len (str): length of a text

    Returns:
        max_tokens: int
    """
    max_tokens = 0
    if 2049 - text_len >= 300:
        max_tokens = 200
    elif 2049 - text_len >= 200:
        max_tokens = 100
    elif 2049 - text_len >= 100:
        max_tokens = 50
    else:
        max_tokens = 300
    return max_tokens
