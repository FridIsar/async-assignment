from flask import Flask, request, jsonify
from csv_processing import group_plays_by_song_and_date
from celery_setup import celery_init_app
from celery import shared_task

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)


@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b


@app.route("/schedule", methods=["POST"])
def schedule():
    # Extracting input_path and output_path from the POST request
    input_path = request.form.get("input_path")
    output_path = request.form.get("output_path")
    
    # Check if both input_path and output_path are provided
    if not input_path or not output_path:
        return jsonify({"error": "Missing input_path or output_path"}), 400
    
    # Try to process the files
    try:
        group_plays_by_song_and_date(input_path, output_path)
        pid = 1  # Dummy process ID to indicate success, you can replace it with actual logic
        return jsonify({"pid": pid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500