import hashlib
import math
import socketio
import redis

from progress.bar import IncrementalBar


REDIS_STORE_CONN_URI = "redis://localhost:6379/0"
redis_store = redis.Redis.from_url(REDIS_STORE_CONN_URI)


def custom_copyfileobj(fsrc, fdst, file_size):

    channel = redis_store.pubsub()

    bar = IncrementalBar('Countdown', max=100)

    block_size = 2 ** 20
    cur_block_pos = 0
    iter_count = 1
    progress_in_percent = 0
    # File uploading in parts
    while True:
        cur_block = fsrc.read(block_size)
        cur_block_pos += block_size
        if not cur_block:
            break
        else:
            fdst.write(cur_block)

        iter_count += 1

        bar_iter = 100 * block_size * iter_count / \
            file_size - float(progress_in_percent)

        progress_in_percent = 100 * block_size * iter_count / file_size
        progress_in_percent = '{0:.2f}'.format(progress_in_percent)
        if float(progress_in_percent) <= 100.00:
            bar.next(bar_iter)
            redis_store.publish('download_file_progress', progress_in_percent)
            # print(progress_in_percent)
        else:
            bar.finish()
            # print(100.00)

    return {"File uploaded successfully!"}


def hash_file(file_name):
    h = hashlib.sha256()

    with open(file_name, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()
