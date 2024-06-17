import time
from celery import shared_task
from .data_processing.csv_processing import group_plays_by_song_and_date

@shared_task(ignore_result=False)
def process_files(input_filename: str, output_filename: str) -> str:
    time.sleep(10)
    dir = '/app/example/data_processing/data/csv'
    group_plays_by_song_and_date(f"{dir}/{input_filename}", f"{dir}/{output_filename}")
    return f"example/data_processing/data/{output_filename}"