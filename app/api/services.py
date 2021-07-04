import hashlib


def custom_copyfileobj(fsrc, fdst, file_size):

    block_size = 2 ** 20
    cur_block_pos = 0
    iter_count = 1
    # File uploading in parts
    while True:
        cur_block = fsrc.read(block_size)
        cur_block_pos += block_size
        if not cur_block:
            break
        else:
            fdst.write(cur_block)

        iter_count += 1
        progress_in_percent = 100 * block_size * iter_count / file_size
        progress_in_percent = '{0:.2f}'.format(progress_in_percent)
        if float(progress_in_percent) <= 100.00:
            print(progress_in_percent)
        else:
            print(100.00)

    return {"File uploaded successfully!"}


def hash_file(file_name):
    h = hashlib.sha256()

    with open(file_name, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()
