import json
import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates

# from starlette.datastructures import URL

from utils.youtube import get_video, get_duration
from utils.assemblyai import download_youtube, detect_language, transcribe
from utils.openai import get_openai_summarization
from utils import helper_functions


templates = Jinja2Templates(directory="templates")
# templates.env.globals["URL"] = URL

router = APIRouter(prefix="", tags=["homepage"])


@router.get("/", response_class=HTMLResponse(), tags=["home"])
def homepage(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@router.post("/")
def search_youtube(request: Request, query: str = Form(default="python 3")):
    videos = get_video(query)
    durations = get_duration(videos)
    videos = zip(videos, durations)
    return templates.TemplateResponse(
        "youtube.html",
        context={"request": request, "video": videos},
    )


@router.post("/process")
def get_transcript(request: Request, video: str = Form(...)):
    text, title, thumbnail = helper_functions.download_vido(
        download_youtube, detect_language, transcribe, video
    )
    file_data = helper_functions.read_file("templates/process.txt")
    input_data = file_data.replace("<<TEXT>>", text)
    # text_len = len(input_data.split())
    response = (
        get_openai_summarization(prompt=input_data, max_tokens=400, temperature=0.7)
        .choices[0]
        .text
    )
    return templates.TemplateResponse(
        "process.html",
        context={
            "request": request,
            "transcript": text,
            "response": response,
            "title": title,
            "thumbnail": thumbnail,
        },
    )


@router.post("/transcript")
def get_text(request: Request, video: str = Form(...)):
    text, title, thumbnail = helper_functions.download_vido(
        download_youtube, detect_language, transcribe, video
    )

    return templates.TemplateResponse(
        "text.html",
        context={
            "request": request,
            "transcript": text,
            "title": title,
            "thumbnail": thumbnail,
        },
    )
