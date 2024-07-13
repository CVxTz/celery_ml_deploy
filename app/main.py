import os

import uvicorn
from fastapi import FastAPI
from nicegui import ui
from page import home


def init(fastapi_app: FastAPI) -> None:
    ui.page("/", title="Image captioning tool")(home)

    ui.run_with(
        fastapi_app,
        mount_path="/",  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret=os.getenv("STORAGE", "__STORAGE__"),
    )


app = FastAPI()

init(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
