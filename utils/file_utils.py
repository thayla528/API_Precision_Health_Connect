import os
import uuid
from werkzeug.utils import secure_filename
import config


def allowed_file(filename):
    """Valida se a extensão do arquivo enviado é permitida."""
    if not filename or "." not in filename:
        return False

    # Extrai a extensão de forma segura
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in config.ALLOWED_EXTENSIONS


def save_profile_photo(file):
    """Salva a foto de perfil na pasta uploads/profile_photos e retorna o nome limpo."""
    if not file or not file.filename or not allowed_file(file.filename):
        return None

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filename = secure_filename(filename)

    # Coleta a pasta direto do módulo config de forma segura
    folder = getattr(config, "PROFILE_PHOTOS_FOLDER", os.path.join(config.UPLOAD_FOLDER, "profile_photos"))
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, filename)
    file.save(filepath)

    return filename


def save_document(file):
    """Salva documentos gerais na pasta uploads/documents e retorna o nome limpo."""
    if not file or not file.filename or not allowed_file(file.filename):
        return None

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filename = secure_filename(filename)

    folder = config.DOCUMENT_FOLDER
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, filename)
    file.save(filepath)

    return filename
