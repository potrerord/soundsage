from typing import List
import numpy as np

class Song:
    def __init__(self, track_id: str, name: str, album: str, album_id: str, 
                 artists: List[str], artist_ids: List[str], track_number: int, 
                 disc_number: int, explicit: bool, danceability: float, energy: float, 
                 key: int, loudness: float, mode: int, speechiness: float, 
                 acousticness: float, instrumentalness: float, liveness: float, 
                 valence: float, tempo: float, duration_ms: int, time_signature: float, 
                 year: int, release_date: str):
        self.track_id = track_id
        self.name = name
        self.album = album
        self.album_id = album_id
        self.artists = artists
        self.artist_ids = artist_ids
        self.track_number = track_number
        self.disc_number = disc_number
        self.explicit = explicit
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.duration_ms = duration_ms
        self.time_signature = time_signature
        self.year = year
        self.release_date = release_date

    def to_vector(self):
        """
        Converts the song's features into a numerical vector for cosine similarity calculation.
        """
        return np.array([self.danceability, self.energy, self.valence, self.acousticness, self.tempo, self.loudness])
    def __repr__(self):
        return (f"Song(track_id={self.track_id}, danceability={self.danceability}, "
                f"energy={self.energy}, valence={self.valence}, genres={self.genres}, artist={self.artist})")