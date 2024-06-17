import os
import sqlite3

import pandas as pd


class BufferDB:
    def __init__(self):
        self.db_file = f"buffer-{os.urandom(8).hex()}.db"
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()
        self.cur.execute("DROP TABLE IF EXISTS buffer")
        self.cur.execute(
            """CREATE TABLE buffer (
            song TEXT,
            date TEXT,
            plays INTEGER,
            PRIMARY KEY (song, date)
            )"""
        )
        self.con.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        self.con.close()

    def add_plays_or_create_row(self, song: str, date: str, str_plays: str):
        plays = int(str_plays)
        # Insert or update the record
        self.cur.execute(
            """
            INSERT INTO buffer (song, date, plays)
            VALUES (?, ?, ?)
            ON CONFLICT(song, date)
            DO UPDATE SET plays = plays + excluded.plays
        """,
            (song, date, plays),
        )
        self.con.commit()

    def streamTo(self, f_out):
        # Write the column headers
        f_out.write("Song,Date,Total Number of Plays for Date\n")

        query = "SELECT * FROM buffer ORDER BY song, date"

        # Read and write the data in chunks
        for chunk in pd.read_sql_query(query, self.con, chunksize=10000):
            chunk.to_csv(f_out, index=False, header=False)
