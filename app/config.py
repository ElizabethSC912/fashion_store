import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = "fashion_store_2026"

    SQLALCHEMY_DATABASE_URI = "sqlite:///fashion_store.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads")