import typing
import pathlib
import csv
from db import BufferDB


def process_files(input_path: str, output_path: str):
    with open(pathlib.Path(input_path), "r") as f_in, open(pathlib.Path(output_path), "w") as f_out:
        group_song_by_date(f_in, f_out)


def group_song_by_date(f_in: typing.TextIO, f_out: typing.TextIO):
    buffer = BufferDB()
    reader = csv.DictReader(f_in)
    for row in reader:
        buffer.add_plays_or_create_row(
            row["Song"],
            row["Date"],
            row["Number of Plays"]
        )
    buffer.streamTo(f_out)


def main():
    process_files("data/example_input.csv", "data/example_output.csv")


if __name__ == "__main__":
    main()
