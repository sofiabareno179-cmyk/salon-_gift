import os
import secrets

class Config:
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url:
        # Solo está instalado psycopg v3 (no psycopg2): normaliza el esquema
        if _db_url.startswith('postgresql://'):
            _db_url = _db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://admin:9027865@postgres-db-c38d7vwnqgy3163y3q7q9z10:5432/salonglitt_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(24)
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads', 'servicios')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max limit