import os
import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://admin:9027865@127.0.0.1:500/salonglitt_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(24)
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads', 'servicios')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max limit