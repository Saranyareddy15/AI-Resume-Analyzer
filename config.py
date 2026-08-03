
import os

# --- Flask ---
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# --- MySQL ---
# Update these to match your local MySQL setup.
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "yourrealpassword"),
    "database": os.environ.get("DB_NAME", "resume_analyzer"),
}

# --- Uploads ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
