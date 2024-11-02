import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-strong-random-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Limit uploads to 2MB
    DEBUG = True
