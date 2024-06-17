import os

from flask import Blueprint
from flask import __version__
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import redirect
from celery.result import AsyncResult

from .logging_config import configure_logging
from ..tasks import process_files

from config.settings import DEBUG

page = Blueprint("page", __name__, template_folder="templates")

# Configure logging
logger = configure_logging()

def render_homepage(*args, **kwargs):
    return render_template(
        "page/home.html",
        flask_ver=__version__,
        python_ver=os.environ["PYTHON_VERSION"],
        debug=DEBUG,
        **kwargs
    )

@page.get("/")
def home():
    return render_homepage()
    
@page.post("/schedule")
def schedule():
    input_file = request.form.get("input_file")
    output_file = request.form.get("output_file")
    
    # Call the Celery task asynchronously and get the task ID
    task = process_files.delay(input_file, output_file)
    task_id = task.id
    message = f"Task {task_id} has been scheduled."
    
    logger.info(message)
    
    # Respond to indicate the task is scheduled
    return render_homepage(id=task_id, message=message)
    
@page.get("/download")
def download() -> dict[str, object]:
    id = request.args.get("process_id")
    result = AsyncResult(id)
    result_status = {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
    return render_homepage(id=id, result_status=result_status)