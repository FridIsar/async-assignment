import typing
import pathlib
import csv
from db import BufferDB


def group_plays_by_song_and_date(input_path: str, output_path: str):
    with open(pathlib.Path(input_path), "r") as f_in, open(pathlib.Path(output_path), "w") as f_out:
        group_plays_by_song_and_date_io(f_in, f_out)


def group_plays_by_song_and_date_io(f_in: typing.TextIO, f_out: typing.TextIO):
    reader = csv.DictReader(f_in)
    
    with BufferDB() as buffer:
        for row in reader:
            buffer.add_plays_or_create_row(
                row["Song"],
                row["Date"],
                row["Number of Plays"]
            )
        buffer.streamTo(f_out)


def main():
    group_plays_by_song_and_date("data/example_input.csv", "data/example_output.csv")


if __name__ == "__main__":
    main()
