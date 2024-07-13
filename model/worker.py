import os

from celery import Celery
from loguru import logger

from model import run_inference

# Get Redis URL from environment variable or use default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Configure Celery to use Redis as the broker and backend
app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)
# Configure the result expiration time to 1 hour (3600 seconds)
app.conf.update(result_expires=1200)


# Register the function run_inference with Celery
@app.task(bind=True, max_retries=3)
def inference_task(self, url, task_prompt):
    logger.info(f"Executing task for {url=}")
    try:
        logger.info(f"Running Inference {url=}")
        return run_inference(url, task_prompt)
    except Exception as exc:
        logger.exception(f"Exception for task where {url=}")
        raise self.retry(exc=exc)


if __name__ == "__main__":
    app.worker_main(["worker", "--loglevel=info", "--pool=solo"])
