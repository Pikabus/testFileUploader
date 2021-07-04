import requests

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from app.celery_app.tasks import download_file_task
from app.api.services import custom_copyfileobj


file_uploader_router = APIRouter()


@file_uploader_router.post("/upload_file")
def upload_file(file_size: int, files: List[UploadFile] = File(...)):
    # Upload multiple files
    for file in files:
        with open(f"files/{file.filename}", "wb") as buffer:
            custom_copyfileobj(file.file, buffer, file_size)
    return {"File uploaded successfully!"}


@file_uploader_router.post("/download_file")
def download_file(url: str):
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
    return {"Accepted!"}
