from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .api.uploader import file_uploader_router


app = FastAPI(title="File uploader API")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    file_uploader_router,
    prefix="",
    tags=["FileUploader"],
)
