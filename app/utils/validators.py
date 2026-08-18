from pathlib import Path

from app.config.settings import settings

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}


def validate_upload(file_name: str | None, file_size: int | None) -> tuple[bool, str | None]:
    if not file_name:
        return False, "Please select a prescription file."
    extension = Path(file_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return False, "Please upload a JPG, PNG, or PDF prescription."
    if file_size is None or file_size <= 0:
        return False, "Upload is empty. Please try again."
    if file_size > settings.MAX_UPLOAD_SIZE:
        return False, "The file is too large. Please upload a smaller prescription."
    return True, None


def sanitize_filename(filename: str) -> str:
    safe_name = Path(filename).name
    safe_name = safe_name.replace(" ", "_")
    return safe_name


def get_upload_directory() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir
