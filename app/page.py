from nicegui import ui
from utils import PageData, handle_upload


def home():
    page_data = PageData()

    # User Interface
    with ui.row().style(
        "justify-content: center; align-items: center; gap: 10em"
    ).classes("w-full"):
        with ui.column().style("align-items: center;").classes("w-full"):
            ui.label("Image Upload").classes("text-2xl")
            upload = (
                ui.upload(
                    auto_upload=True,
                    max_files=1,
                    max_file_size=1024 * 1024 * 4,
                    on_upload=lambda e: handle_upload(
                        e=e, upload_reset=upload.reset, data=page_data
                    ),
                    on_rejected=lambda: ui.notify(
                        "Rejected! File too large", type="negative"
                    ),
                )
                .classes("w-4/12 bg-slate-100")
                .props('accept=".png, image/*"')
            )
            with ui.card().classes(
                "relative w-4/12 h-96 overflow-hidden bg-slate-100"
            ).bind_visibility_from(page_data, "image_content"):
                ui.image().classes(
                    "absolute inset-0 w-full h-full object-cover"
                ).bind_source_from(page_data, "image_content")

            with ui.card().classes().bind_visibility_from(
                page_data, "image_content"
            ).classes("w-4/12 bg-slate-100"):
                ui.skeleton().classes("w-full").bind_visibility_from(
                    page_data, "caption", backward=lambda x: x is None
                )
                ui.label().bind_text_from(page_data, "caption")

    with ui.footer().classes("bg-slate-100 rounded-lg shadow m-4 dark:bg-gray-800"):
        with ui.row().classes(
            "w-full justify-center items-center gap-10 text-white font-bold"
        ):
            ui.link(
                "Linkedin", "https://www.linkedin.com/in/mansar/", new_tab=True
            ).classes("text-black no-underline")
            ui.link(
                "Source Code", "https://github.com/CVxTz/celery_ml_deploy", new_tab=True
            ).classes("text-black no-underline")
