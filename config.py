import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

DOCUMENT_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "documents"
)

MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}