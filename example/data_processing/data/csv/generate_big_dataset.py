import csv
import random
import string
import datetime

# Define number of rows and unique song names
num_rows = 10000000
num_unique_songs = 100000

# Function to generate random song names
def generate_song_name(length=10):
  """Generates a random song name of specified length."""
  letters = string.ascii_lowercase + string.digits + " "  # Allowed characters
  return ''.join(random.choice(letters) for _ in range(length))

# Open the file in write mode with buffering
with open("very_large_data.csv", "w", newline="", buffering=1) as csvfile:
  writer = csv.writer(csvfile)

  # Write the header row
  writer.writerow(["Song", "Date", "Number of Plays"])

  # Generate a pool of unique song names beforehand
  unique_songs = set(generate_song_name() for _ in range(num_unique_songs))

  # Generate and write data rows
  for _ in range(num_rows):
    # Choose a random song name from the pool
    song = random.choice(list(unique_songs))
    date = datetime.datetime(2020, random.randint(1, 12), random.randint(1, 28)).strftime('%Y-%m-%d')
    plays = random.randint(50, 1000)
    writer.writerow([song, date, plays])

  print("Very large CSV file generated successfully!")
