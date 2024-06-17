import pandas as pd
import pathlib
import os

from csv_processing import group_song_by_date

def test_group_song_by_date():
    # Define the paths for input and output files
    input_file = "data/example_input.csv"
    output_file = "data/example_output.csv"
    expected_output_file = "data/example_expected_output.csv"
    
    # Clear the output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Call the function to test
    with open(pathlib.Path(input_file), "r") as f_in, open(pathlib.Path(output_file), "w") as f_out:
        group_song_by_date(f_in, f_out)

    # Read the output file and expected output file into DataFrames
    output_df = pd.read_csv(output_file)
    expected_output_df = pd.read_csv(expected_output_file)

    # Compare the DataFrames
    pd.testing.assert_frame_equal(output_df, expected_output_df)