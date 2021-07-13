import socketio
import time
import redis

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from .api.uploader import file_uploader_router
from app.config import REDIS_STORE_CONN_URI


REDIS_STORE_CONN_URI = "redis://localhost:6379/0"
redis_store = redis.Redis.from_url(REDIS_STORE_CONN_URI)


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


def custom_handler(message):
    message_data = message['data']
    app.sio.emit('download_file_progress', {'data': f'{message_data}'})


@app.sio.on('download_file')
async def download_file(sid, *args, **kwargs):
    sub = redis_store.pubsub()

    sub.psubscribe(**{'download_file_progress': custom_handler})
    thread = sub.run_in_thread(sleep_time=0.001)

    # thread.stop()
