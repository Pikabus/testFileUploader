import shutil
# import redis
import requests

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
from celery import Celery


file_uploader_router = APIRouter()


@file_uploader_router.post("/upload_file")
def upload_file(file_size: int, files: List[UploadFile] = File(...)):
    # Upload multiple files
    for file in files:
        with open(f"../../files/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"state": "Files uploaded successfully!"}


@file_uploader_router.post("/download_file")
def download_file(url: str):
    try:
        response = requests.get(url, stream=True)
    except:
        return {"state": "Error, incorrect url or file doesn't exists!"}

    # If URL correct
    file_size = int(response.headers.get("content-length", 0))
    if file_size == 0:
        return {"Error, file not found!"}

    # If URL correct and file exists
    file_name = response.headers.get("Content-Disposition", url[-10:])
    file_name = file_name.replace("attachment; filename=", "")

    # Save file
    with open(f"../../files/{file_name}", "wb") as file:
        file.write()

    return {"File uploaded successfully!"}
