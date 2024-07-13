import base64
import hashlib
import os
import uuid
from pathlib import Path
from typing import Optional

from client import send_inference_task
from google.cloud import storage
from loguru import logger
from nicegui import run, ui
from nicegui.events import UploadEventArguments

FILES_BASE_PATH = os.getenv("FILES_BASE_PATH", "/tmp")

TASK_PROMPT = "<MORE_DETAILED_CAPTION>"


class PageData:
    def __init__(self, image_content=None, image_path=None, caption=None):
        self.image_content: Optional[str] = image_content
        self.image_path: Optional[str] = image_path
        self.caption: Optional[str] = caption

    def reset(self):
        self.image_content = None
        self.image_path = None
        self.caption = None


def hash_to_uuid(binary_content: bytes) -> uuid.UUID:
    """
    Hashes the binary content deterministically to a UUID.

    Args:
        binary_content (bytes): The binary content to hash.

    Returns:
        uuid.UUID: A UUID generated from the hash of the binary content.
    """
    hash_obj = hashlib.sha256(binary_content)
    hash_hex = hash_obj.hexdigest()
    return uuid.UUID(hash_hex[:32])  # Use the first 32 characters to form a valid UUID


def save_file(binary_content: bytes, file_extension: str, base_path: str) -> str:
    """
    Saves the binary content to a file and returns the file path.

    Args:
        binary_content (bytes): The binary content to save.
        file_extension (str): The file extension (e.g., '.jpg').
        base_path (str): The base directory where the file should be saved.

    Returns:
        str: The file path where the content was saved.
    """
    unique_uuid = hash_to_uuid(binary_content)
    unique_filename = f"{unique_uuid}{file_extension}"

    if base_path.startswith("gs://"):
        # Extract bucket name and optional directory from base_path
        bucket_name, _, directory = base_path[5:].partition("/")
        if directory:
            blob_name = f"{directory.rstrip('/')}/{unique_filename}"
        else:
            blob_name = unique_filename

        # Initialize a client and upload the file to the bucket
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(binary_content)

        return f"gs://{bucket_name}/{blob_name}"
    else:
        file_path = Path(base_path) / unique_filename

        with file_path.open("wb") as f:
            f.write(binary_content)

        return str(file_path)


async def handle_upload(
    e: UploadEventArguments, upload_reset: callable, data: PageData
):
    data.reset()

    logger.info("Reading image content")

    image_data = e.content.read()
    b64_bytes = base64.b64encode(image_data)
    data.image_content = f"data:{e.type};base64,{b64_bytes.decode()}"

    upload_reset()

    file_extension = Path(e.name).suffix
    file_path = await run.io_bound(
        save_file, image_data, file_extension, FILES_BASE_PATH
    )

    data.image_path = file_path

    logger.info("Generating caption")

    result = await run.io_bound(send_inference_task, data.image_path, TASK_PROMPT)

    logger.info("Displaying caption")

    data.caption = result[TASK_PROMPT]

    ui.notify("Image captioned!", type="positive")
