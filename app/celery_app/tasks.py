import os
import requests
import redis

from celery import current_task

from .worker import celery
from app.api.services import hash_file
from app.config import REDIS_STORE_CONN_URI


REDIS_STORE_CONN_URI = "redis://localhost:6379/0"
redis_store = redis.Redis.from_url(REDIS_STORE_CONN_URI)


@celery.task(serializer='json')
def download_file_task(url: str, file_size: int):
    file_full_name = url.split('/')[-1]

    # Define file full name
    file_name = file_full_name[:file_full_name.find(".")]
    if file_full_name.find(".") != -1:
        file_extension = file_full_name[file_full_name.find(".")+1:]
    else:
        file_extension = ""
    file_full_name = str(file_name) + "." + str(file_extension)

    # Define file name. If this file name exists: file name += "file_name (копия name_counter).file_extension"
    name_counter = 0
    while True:
        if file_full_name in os.listdir("files/"):
            file_name = file_name.replace(f" (копия {name_counter})", "")
            name_counter += 1
            file_name += f" (копия {name_counter})"
            file_full_name = file_name + "." + file_extension
        else:
            break

    # Download file and shows it progress
    chunk_size = 2 ** 20
    iter_count = 1
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(f"files/{file_full_name}", "wb") as file:
            for chunk in response.iter_content(chunk_size):
                # Print downloading progress and write file in parts
                progress_in_percent = 100 * iter_count * chunk_size / file_size
                if progress_in_percent <= 100:
                    current_task.update_state(state='PROGRESS', meta={
                                              'process_percent': '{0:.2f}'.format(progress_in_percent)})
                    # print('{0:.2f}'.format(progress_in_percent))
                iter_count += 1

                file.write(chunk)
    # print(100.00)

    ps = redis_store.pubsub()
    ps.subscribe('abc')
    for msg in ps.listen():
        print(msg)

    download_file_task.update_state(
        state='PROGRESS', meta={'process_percent': '100.00'})

    # Delete file if it hash exists
    file_hash = str(hash_file(f"files/{file_full_name}"))
    if redis_store.get(file_hash) is not None:
        os.remove(f"files/{file_full_name}")
    else:
        redis_store.set(file_hash, file_full_name)
    return {"status": "File uploaded successfully!"}
