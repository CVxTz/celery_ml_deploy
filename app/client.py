import os

from celery import Celery

# Import the task from the worker

# Get Redis URL from environment variable or use default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Configure Celery to use Redis as the broker and backend
app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)
# Configure the result expiration time to 1 hour (3600 seconds)
app.conf.update(result_expires=3600)

task_name = "tasks.inference_task"
inference_task = app.signature(task_name)


def send_inference_task(url, task_prompt):
    """
    Send an inference task to the worker and wait for the result.

    :param url: The image url to be processed.
    :param task_prompt: The task prompt for the inference.
    :return: The result of the inference task.
    """
    task = inference_task.delay(url, task_prompt)
    print(f"Task sent with ID: {task.id}")

    # Wait for the result
    result = task.get(timeout=120)
    return result


if __name__ == "__main__":
    # Example usage
    _url = "https://picsum.photos/id/237/200/300"

    _task_prompt = "<DETAILED_CAPTION>"

    _result = send_inference_task(url=_url, task_prompt=_task_prompt)
    print(f"Task result: {_result}")
