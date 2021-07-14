import hashlib


def hash_file(file_name):
    h = hashlib.sha256()

    with open(file_name, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()
