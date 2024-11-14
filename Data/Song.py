from typing import List
import numpy as np

class Song:
    def __init__(self, track_id: str, danceability: float, energy: float, valence: float,
                 acousticness: float, tempo: float, loudness: float,
                 genres: List[str], artist: str):
        self.track_id = track_id
        self.danceability = danceability
        self.energy = energy
        self.valence = valence
        self.acousticness = acousticness
        self.tempo = tempo
        self.loudness = loudness
        self.genres = genres
        self.artist = artist

    def to_vector(self):
        """
        Converts the song's features into a numerical vector for cosine similarity calculation.
        """
        return np.array([self.danceability, self.energy, self.valence, self.acousticness, self.tempo, self.loudness])
    def __repr__(self):
        return (f"Song(track_id={self.track_id}, danceability={self.danceability}, "
                f"energy={self.energy}, valence={self.valence}, genres={self.genres}, artist={self.artist})")