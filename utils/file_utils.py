import os

import uuid

from werkzeug.utils import secure_filename

from config import (
    DOCUMENT_FOLDER,
    ALLOWED_EXTENSIONS
)


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def save_document(file):

    if not allowed_file(file.filename):

        return None


    extension = (
        file.filename
        .rsplit(".", 1)[1]
        .lower()
    )


    filename = (
        f"{uuid.uuid4()}.{extension}"
    )


    filename = secure_filename(
        filename
    )


    os.makedirs(
        DOCUMENT_FOLDER,
        exist_ok=True
    )


    filepath = os.path.join(
        DOCUMENT_FOLDER,
        filename
    )


    file.save(filepath)


    return filepath