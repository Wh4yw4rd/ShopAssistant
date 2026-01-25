from dotenv import load_dotenv
import os

load_dotenv(".env")

db_config = {
    "host":os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT"),
    "database":os.getenv("DB_NAME"),
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD")
}

sumup_api = {
    "key": os.getenv("SUMUP_API_KEY"),
    "merchant_code": os.getenv("MERCHANT_CODE")
}