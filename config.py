import os
import sys
import shutil

APP_NAME = "DataCollect"  # rename if needed

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Example Google Sheet ID (keep or override via env var)
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1ducwMEA-YrN9BAD6VJ-a9xNIxLr6wqNbVkg_7_UKggs")

# Detect if running from PyInstaller bundle
if getattr(sys, "frozen", False):
    bundle_dir = sys._MEIPASS  # PyInstaller unpack dir
else:
    bundle_dir = BASE_DIR

# --- Choose user_dir depending on environment ---
if os.getenv("RENDER"):  
    # Render persistent disk
    user_dir = os.path.join("/opt/render/.data", APP_NAME)
elif os.name == "nt":  
    # Windows desktop
    user_dir = os.path.join(os.environ["USERPROFILE"], "Documents", APP_NAME)
else:  
    # Linux/Mac desktop
    user_dir = os.path.join(os.path.expanduser("~"), f".{APP_NAME.lower()}")

os.makedirs(user_dir, exist_ok=True)

# Path to runtime database
RUNTIME_DB_PATH = os.path.join(user_dir, "app.sqlite")

# Copy starter DB from bundle if not already there
if not os.path.exists(RUNTIME_DB_PATH):
    bundled_db = os.path.join(bundle_dir, "instance", "app.sqlite")
    if os.path.exists(bundled_db):
        shutil.copy(bundled_db, RUNTIME_DB_PATH)
        print(f"Copied starter database to {RUNTIME_DB_PATH}")
    else:
        print("No bundled database found; starting fresh.")

# --- Config Classes ---
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")  # change in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{RUNTIME_DB_PATH}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    # Prefer DATABASE_URL (e.g., Postgres on Render), else fallback to SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{RUNTIME_DB_PATH}")