import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_SQL_CONN_STR = os.getenv("AZURE_SQL_CONN_STR")
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING")
