import logging
from azure.storage.blob import BlobServiceClient
from config.config import config

logger = logging.getLogger(__name__)

def upload_file_to_blob(file_stream, file_name: str) -> str:
    """
    Upload a file to Azure Blob Storage and return its URL.
    """
    blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONN_STRING)
    container_name = "feedback-uploads"
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.get_container_properties()
    except Exception as e:
        logger.info(f"Container '{container_name}' does not exist; creating container. ({e})")
        container_client.create_container()
    blob_client = container_client.get_blob_client(file_name)
    try:
        blob_client.upload_blob(file_stream, overwrite=True)
    except Exception as e:
        logger.error(f"Failed to upload blob: {e}")
        raise
    blob_url = blob_client.url
    logger.info(f"File uploaded to blob URL: {blob_url}")
    return blob_url
