import os
from uuid import uuid4

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file) -> str:
    ext = os.path.splitext(upload_file.filename)[1]
    filename = f"{uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return path
