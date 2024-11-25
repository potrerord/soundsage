import csv
from typing import List
import ast
import os
from Data.Song import Song

class SongStore:
    def __init__(self, file_name: str):
        """
        Initializes the SongStore with the given CSV file path.

        :param file_name: The name of the CSV file (e.g., 'tracks_features.csv').
        """
        self.file_path = os.path.join('Data', file_name)  # Combine folder and file name
        self.songs = self._load_songs()

    def _load_songs(self) -> List[Song]:
        """
        Loads songs from the CSV file and returns a list of Song objects.

        :return: A list of Song instances.
        """
        print("attempting to load songs")
        songs = []
        try:
            with open(self.file_path, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    song = Song(
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
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
        return songs

    def _parse_list(self, field: str) -> List[str]:
        """
        Helper method to parse string fields that represent lists (e.g., ['Rage Against The Machine']).

        :param field: A string representation of a list (e.g., "['Artist1', 'Artist2']")
        :return: A list of strings.
        """
        try:
            return ast.literal_eval(field)
        except:
            return []

    def get_all_songs(self) -> List[Song]:
        """
        Returns the list of all songs.

        :return: A list of all Song instances.
        """
        return self.songs

    def get_song_by_id(self, track_id: str) -> Song:
        """
        Returns a song based on its track_id.

        :param track_id: The unique track ID of the song.
        :return: The Song instance with the matching track ID, or None if not found.
        """
        for song in self.songs:
            if song.track_id == track_id:
                return song
        return None