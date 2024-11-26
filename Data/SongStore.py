import csv
import ast
import os
from io import TextIOWrapper
from typing import TextIO

from Data.Song import Song
import Data.constants as c


class SongStore:
    DATA_DIRNAME: str = "Data"

    file_path: str
    songs: list[Song]

    def __init__(
            self: "SongStore",
            file_name: str,
    ) -> None:
        """
        Initializes the SongStore with the given CSV file path.

        :param file_name: The name of the CSV file (e.g., 'tracks_features.csv').
        """
        self.file_path = os.path.join(self.DATA_DIRNAME, file_name)  # Combine folder and file name
        self.songs = self._load_songs()

    def _load_songs(self: "SongStore") -> list[Song]:
        """
        Loads songs from the CSV file and returns a list of Song objects.

        :return: A list of Song instances.
        """
        print(f'\nBeginning data load from "{self.file_path}"...')
        songs: list[Song] = []

        file: TextIO
        with open(self.file_path, newline='', encoding='utf-8') as file:
            # Count the number of data points.
            total_songs = sum(1 for _ in file) - 1
            file.seek(0)

            reader: csv.DictReader = csv.DictReader(file)

            row: dict[str, str]
            i: int = 0
            invalid_song_count: int = 0
            for row in reader:
                i += 1
                print(f"\r ({i / total_songs:.0%}) Loading song {i:,} of {total_songs:,} ({invalid_song_count:,} invalid songs discarded)...", end="")
                
                try:
                    song: Song = Song(
                        track_id=row['id'],
                        name=row['name'],
                        album=row['album'],
                        album_id=row['album_id'],
                        artists=self._parse_list(row['artists']),
                        artist_ids=self._parse_list(row['artist_ids']),
                        track_number=int(row['track_number']),
                        disc_number=int(row['disc_number']),
                        explicit=row['explicit'].lower() == 'true',
                        danceability=float(row['danceability']),
                        energy=float(row['energy']),
                        key=int(row['key']),
                        loudness=float(row['loudness']),
                        mode=int(row['mode']),
                        speechiness=float(row['speechiness']),
                        acousticness=float(row['acousticness']),
                        instrumentalness=float(row['instrumentalness']),
                        liveness=float(row['liveness']),
                        valence=float(row['valence']),
                        tempo=float(row['tempo']),
                        duration_ms=int(row['duration_ms']),
                        time_signature=float(row['time_signature']),
                        year=int(row['year']),
                        release_date=row['release_date']
                    )
                    songs.append(song)
                except ValueError:
                    invalid_song_count += 1

        print(f'\nSuccessfully loaded {len(songs):,} of {total_songs:,} songs from "{self.file_path}".')

        return songs

    def _parse_list(
            self: "SongStore",
            field: str,
    ) -> list[str]:
        """
        Helper method to parse string fields that represent lists (e.g., ['Rage Against The Machine']).

        :param field: A string representation of a list (e.g., "['Artist1', 'Artist2']")
        :return: A list of strings.
        """
        try:
            return ast.literal_eval(field)
        except Exception:
            return []

    def get_all_songs(self: "SongStore") -> list[Song]:
        """
        Returns the list of all songs.

        :return: A list of all Song instances.
        """
        return self.songs

    def get_song_by_id(
            self: "SongStore",
            track_id: str,
    ) -> Song | None:
        """
        Returns a song based on its track_id.

        :param track_id: The unique track ID of the song.
        :return: The Song instance with the matching track ID, or None if not found.
        """
        for song in self.songs:
            if song.track_id == track_id:
                return song
        return None
