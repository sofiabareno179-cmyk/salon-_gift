import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / 'app' / '.env')

class Config:
    SQLITE_PATH = BASE_DIR / 'instance' / 'salonglitt.sqlite'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLITE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(24))
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads', 'servicios')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max limit