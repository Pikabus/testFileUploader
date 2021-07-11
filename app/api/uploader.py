import requests
import redis
import pathlib

from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket, status
from typing import List

from app.celery_app.tasks import download_file_task
from app.api.services import custom_copyfileobj, hash_file
from app.api.schemas import URL
from app.config import REDIS_STORE_CONN_URI


REDIS_STORE_CONN_URI = "redis://localhost:6379/0"
redis_store = redis.Redis.from_url(REDIS_STORE_CONN_URI)

file_uploader_router = APIRouter()


@file_uploader_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text(f"Progress bar: {100} %")


@file_uploader_router.post("/upload_file")
def upload_file(file_size: int, files: List[UploadFile] = File(...)):
    # Upload multiple files
    for file in files:
        # Define file full name
        file_full_name = file.filename
        file_name = file_full_name[:file_full_name.find(".")]
        if file_full_name.find(".") != -1:
            file_extension = file_full_name[file_full_name.find(".")+1:]
        else:
            file_extension = ""
        file_full_name = str(file_name) + "." + str(file_extension)

        # Define file name. If this file name exists: file name += "file name (копия name_counter)"
        name_counter = 0
        while True:
            if redis_store.get(file_full_name) is not None:
                file_name = file_name.replace(f" (копия {name_counter})", "")
                name_counter += 1
                file_name += f" (копия {name_counter})"
                file_full_name = file_name + "." + file_extension
            else:
                break
        # Upload file on server
        with open(f"files/{file_full_name}", "wb") as buffer:
            custom_copyfileobj(file.file, buffer, file_size)

        # Delete file if it hash exists
        file_hash = str(hash_file(f"files/{file_full_name}"))
        if redis_store.get(file_hash) is not None:
            file = pathlib.Path(f"files/{file_full_name}")
            file.unlink()
        else:
            redis_store.set(file_hash, file_full_name)
            redis_store.set(file_full_name, file_hash)
    return {"File uploaded successfully!"}


@file_uploader_router.post("/download_file", status_code=status.HTTP_202_ACCEPTED)
def download_file(url: URL):
    url = url.url
    try:
        response = requests.get(url, stream=True)
    except:
        raise HTTPException(
            status_code=400, detail="Error, incorrect URL or file doesn't exists!")
    # If URL correct
    file_size = int(response.headers.get("content-length", 0))
    if file_size <= 0:
        raise HTTPException(
            status_code=404, detail="Error, file doesn't exists!")
    # If URL correct and file exists
    download_file_task.delay(url, file_size)
    return {"status": "Accepted!"}
