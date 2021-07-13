import socketio
import time

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from .api.uploader import file_uploader_router, redis_store


app = FastAPI(title="File uploader API")
sio = SocketManager(app=app, cors_allowed_origins=[])


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


@app.sio.on('connect')
async def handle_join(sid, *args, **kwargs):
    print(sid, ' connected')


# Shows progress of download file from URL
@app.sio.on('download_file')
async def download_file(sid, *args, **kwargs):
    time.sleep(10)
    p = redis_store.pubsub()
    p.subscribe('download_file_progress')
    while True:
        message = p.get_message()
        if message:
            await app.sio.emit('download_file_progress', {'data': f'{message}'})
