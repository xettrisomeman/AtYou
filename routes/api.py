from fastapi import FastAPI
from .home import router
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")


# @app.get("/download")
# def download(transcript):
#     """Download text

#     Args:
#         transcript (str): text of video

#     Returns:
#         file: text file
#     """
#     return FileResponse(path=".", filename=f"{transcript}.txt", media_type="text")
