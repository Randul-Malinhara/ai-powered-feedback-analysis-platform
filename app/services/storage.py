from azure.storage.blob import BlobServiceClient
from config import BLOB_CONN_STRING

def upload_file_to_blob(file_stream, file_name: str) -> str:
    """
    Upload file to Azure Blob Storage and return the blob URL.
    """
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
    container_name = "feedback-uploads"
    
    # Ensure container exists (you may wish to create it if it doesn't exist)
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.get_container_properties()
    except Exception:
        container_client.create_container()

    blob_client = container_client.get_blob_client(file_name)
    blob_client.upload_blob(file_stream, overwrite=True)
    
    # Construct the blob URL (adjust based on your storage account's URL format)
    blob_url = f"{blob_client.url}"
    return blob_url
