# SoundSage

SoundSage is a music data analysis tool that allows you to work with song features like danceability, energy, and tempo, among others. This project loads song data from a CSV file and processes it to create user profiles based on their music preferences.

## Requirements

Before using this project, ensure you have the following:

- Python 3.x
- Required libraries:
  - `csv`
  - `typing`

You can install any required libraries using pip:

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. **Insert the CSV file**:
   - Download or provide a CSV file containing the song data.
   - Place the CSV file in a folder named `Data` located in the root directory of the project.
   - The CSV file **must** be named `tracks_features.csv`.