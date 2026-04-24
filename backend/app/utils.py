"""UUID helper functions."""
import uuid


def generate_job_id() -> str:
    """Generate a unique job ID."""
    return str(uuid.uuid4())


def get_file_extension(filename: str) -> str:
    """Extract file extension."""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def is_allowed_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension."""
    return get_file_extension(filename) in allowed_extensions
