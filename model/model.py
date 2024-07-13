import os
from io import BytesIO

import requests
from google.cloud import storage
from loguru import logger
from modeling_florence2 import Florence2ForConditionalGeneration
from PIL import Image
from processing_florence2 import Florence2Processor

model = Florence2ForConditionalGeneration.from_pretrained(
    "microsoft/Florence-2-base-ft"
)
processor = Florence2Processor.from_pretrained("microsoft/Florence-2-base-ft")


def download_image(url):
    if url.startswith("http://") or url.startswith("https://"):
        # Handle HTTP/HTTPS URLs
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            logger.info(
                f"Failed to download image. HTTP Status code: {response.status_code}"
            )
            return None
    elif url.startswith("gs://"):
        # Handle Google Cloud Storage paths
        client = storage.Client()
        bucket_name, blob_name = url[5:].split("/", 1)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        byte_stream = BytesIO()
        blob.download_to_file(byte_stream)
        byte_stream.seek(0)
        return byte_stream
    else:
        # Handle local file paths
        if os.path.exists(url):
            with open(url, "rb") as file:
                return BytesIO(file.read())
        else:
            logger.info(f"Local file not found: {url}")
            return None


def run_inference(url, task_prompt):
    logger.info(f"Downloading image {url=}")

    image_stream = download_image(url)
    try:
        logger.info(f"Opening image {url=}")
        image = Image.open(image_stream).convert("RGB")
        inputs = processor(text=task_prompt, images=image, return_tensors="pt")
    except ValueError:
        logger.exception("Error processing image")
        return {task_prompt: "Invalid Image"}

    logger.info(f"Generate {url=}")
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        num_beams=3,
    )
    logger.info(f"Decode {url=}")

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    logger.info(f"Post Process {url=}")

    parsed_answer = processor.post_process_generation(
        generated_text, task=task_prompt, image_size=(image.width, image.height)
    )

    return parsed_answer


if __name__ == "__main__":
    _url = "https://picsum.photos/id/237/200/300"

    _task_prompt = "<DETAILED_CAPTION>"
    print(run_inference(url=_url, task_prompt=_task_prompt))
