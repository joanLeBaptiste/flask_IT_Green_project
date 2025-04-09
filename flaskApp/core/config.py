import os
from dotenv import load_dotenv

load_dotenv()

# Résout le chemin absolu de la base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sqlite_relative_path = os.getenv("DATABASE_PATH", "sqlite/site.db")
SQLITE_ABS_PATH = os.path.abspath(os.path.join(BASE_DIR, sqlite_relative_path))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_ABS_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
