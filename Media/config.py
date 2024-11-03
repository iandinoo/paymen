import os
import logging
from os import getenv
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv(".env")

API_ID = getenv("API_ID", "20211998")
API_HASH = getenv("API_HASH", "beeeebe74c0c467c47c6ac4a1c9d75b5")

BOT_TOKEN = getenv("BOT_TOKEN", "7425535604:AAGFe5fuwfeRE9XQWtITj8kmhNxTYrH6BA0")

OWNER_ID = [int(x) for x in (os.environ.get("OWNER_ID", "8062228305").split())]

MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://adimfagahran:adimfagahran@cluster0.8kejy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = getenv("DB_NAME", "media")

API_KEY_ATLANTIC = getenv("API_KEY_ATLANTIC", "sUPUI7hly7r6MtKtpLtZAbK89kykU3x42o7H32cUZL97tO7w85av62WatZaYuYAbnuJkVHnesftgRGZBmA0U5tbKqhot1gSpGpng")

BOT_WORKERS = getenv("BOT_WORKERS", "4")

LOG_FILE_NAME = "kantorpos.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
