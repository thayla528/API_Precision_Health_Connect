import os

import uuid

from werkzeug.utils import secure_filename

from config import (
    DOCUMENT_FOLDER,
    ALLOWED_EXTENSIONS
)


class FileService:


    @staticmethod
    def allowed_file(filename):

        return (
            "." in filename
            and
            filename.rsplit(".", 1)[1].lower()
            in ALLOWED_EXTENSIONS
        )


    @staticmethod
    def save_document(file):

        if not FileService.allowed_file(
            file.filename
        ):

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


        file.save(
            filepath
        )


        return filepath


    @staticmethod
    def delete_document(filepath):

        if (
            filepath
            and
            os.path.exists(filepath)
        ):

            os.remove(filepath)

            return True

        return False