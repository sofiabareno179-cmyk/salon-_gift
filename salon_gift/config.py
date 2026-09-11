import os
import secrets

class Config:
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url:
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        _instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        os.makedirs(_instance_dir, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_instance_dir, 'salonglitt.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(24)
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads', 'servicios')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max limit