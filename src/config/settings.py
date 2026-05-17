# third party
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()


URL = (
    "https://nsi.rosminzdrav.ru/api/dataFiles"
    "?identifier=1.2.643.5.1.13.13.11.1461"
    "&version=6.1998"
    "&format=JSON"
)


class Settings:
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

settings = Settings()

DB_SCHEMA = "nsi"

BASE_URL = "https://nsi.rosminzdrav.ru"

DICTIONARY_OID = "1.2.643.5.1.13.13.11.1461"

DOWNLOAD_DIR = Path("data/raw")

MAX_RETRIES = 3

RETRY_DELAY_SECONDS = 2

PAGE_GOTO_TIMEOUT=30000

PAGE_WAIT_FOR_TIMEOUT=1000

PAGE_EXPECT_DOWNLOAD=30000

DROP_DOWN_TIMEOUT=3000

EXTRACT_DIR = Path("data/extracted")

RECORD_SOURCE = "nsi.rosminzdrav.ru"

BATCH_SIZE = 50_000

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_LEVEL = "INFO"

LOG_BACKUP_COUNT = 30

LOG_STORAGE_DAYS = 30

LOG_MAX_FILE_SIZE_MB = 20
