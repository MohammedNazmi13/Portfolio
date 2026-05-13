import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fallback-key')
    
    # Database configuration
    # Vercel/Neon provide a DATABASE_URL. We handle the "postgres://" vs "postgresql://" issue.
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    # Fallback to local SQLite if no DATABASE_URL is found
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join('static', 'uploads', 'certificates')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
