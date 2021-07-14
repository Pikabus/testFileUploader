import socketio
import time
import redis
import asyncio

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from aredis import StrictRedis as AsyncRedis

from .api.uploader import file_uploader_router
from app.config import REDIS_STORE_CONN_URI


REDIS_STORE_CONN_URI = "redis://localhost:6379/0"
redis_store = AsyncRedis.from_url(REDIS_STORE_CONN_URI)


app = FastAPI(title="File uploader API")

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
sio_app = socketio.ASGIApp(socketio_server=sio, socketio_path="socket.io")

app.mount("/ws", sio_app)


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


@sio.on('connect')
async def connect(sid, data):
    print(sid, ' connected')


@sio.on('disconnect')
async def connect(sid):
    print(sid, ' disconnected')


async def emit_progress_bar(pubsub):
    while True:
        message = await pubsub.get_message(timeout=1)
        if message is not None and message['type'] == 'message':
            message_data = message['data']
            message_data = message_data.decode('utf-8')
            await sio.emit('download_file_progress', {
                'detail': {
                    'progress_in_procent': f'{message_data}'
                }
            })
        await asyncio.sleep(0.01)


@ sio.on('download_file')
async def download_file(sid, data):
    pubsub = redis_store.pubsub()

    await pubsub.subscribe('download_file_progress')
    await emit_progress_bar(pubsub)

# .\venv\Scripts\activate
# uvicorn app.main:app
