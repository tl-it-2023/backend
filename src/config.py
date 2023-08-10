import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
STORAGE_RESUME_FILE = os.path.join(STORAGE_PATH, "unsort")

STORAGE_RESUME = os.path.join(STORAGE_PATH, "resume")


def folders_create():
    folders = [STORAGE_PATH, STORAGE_RESUME_FILE, STORAGE_RESUME]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


if __name__ == "__main__":
    folders_create()