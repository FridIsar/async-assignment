import os
import pathlib

import pandas as pd

from project.data_processing.csv_processing import (
    group_plays_by_song_and_date_io,
)


def test_group_plays_by_song_and_date_io():
    # Define the paths for input and output files
    dir = "/app/project/data_processing/data/csv"
    input_file = f"{dir}/example_input.csv"
    output_file = f"{dir}/example_output.csv"
    expected_output_file = f"{dir}/example_expected_output.csv"

    # Clear the output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Call the function to test
    with open(pathlib.Path(input_file), "r") as f_in, open(
        pathlib.Path(output_file), "w"
    ) as f_out:
        group_plays_by_song_and_date_io(f_in, f_out)

    # Read the output file and expected output file into DataFrames
    output_df = pd.read_csv(output_file)
    expected_output_df = pd.read_csv(expected_output_file)

    # Compare the DataFrames
    pd.testing.assert_frame_equal(output_df, expected_output_df)
