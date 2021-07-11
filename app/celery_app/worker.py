from celery import Celery, Task

from app.config import BROKER_CONN_URI, BACKEND_CONN_URI

BROKER_CONN_URI = "pyamqp://guest@localhost//"
BACKEND_CONN_URI = "redis://localhost:6379/0"

celery = Celery('fileploader', broker=BROKER_CONN_URI,
                backend=BACKEND_CONN_URI, include=['app.celery_app.tasks'])
# broker=BROKER_CONN_URI,
# backend=BACKEND_CONN_URI,
