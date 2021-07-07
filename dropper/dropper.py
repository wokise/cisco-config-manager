import base64


def drop_file(path, base64_str):
    with open(path, "wb") as fh:
        fh.write(base64.decodebytes(base64_str))