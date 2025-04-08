import os

class Config:
    # Use an async-supported connection string (here using SQLite for example)
    AZURE_SQL_CONN_STR = os.getenv("AZURE_SQL_CONN_STR", "sqlite+aiosqlite:///./test.db")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "https://<your-resource-name>.cognitiveservices.azure.com/")
    AZURE_KEY = os.getenv("AZURE_KEY", "your_azure_key")
    BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING", "your_blob_conn_string")

config = Config()
