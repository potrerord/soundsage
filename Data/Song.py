import numpy as np

import Data.constants as c

class Song:
    def __init__(
            self,
            track_id: str,
            name: str,
            album: str,
            album_id: str,
            artists: list[str],
            artist_ids: list[str],
            track_number: int,
            disc_number: int,
            explicit: bool,
            danceability: float,
            energy: float,
            key: int,
            loudness: float,
            mode: int,
            speechiness: float,
            acousticness: float,
            instrumentalness: float,
            liveness: float,
            valence: float,
            tempo: float,
            duration_ms: int,
            time_signature: float,
            year: int,
            release_date: str
    ) -> None:
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

    def to_vector(self: "Song") -> np.ndarray[np.shape, np.dtype[np.float64]]:
        """
        Converts the song's features into a numerical vector for cosine similarity calculation.
        """
        return np.array([
            self.danceability,
            self.energy,
            self.valence,
            self.acousticness,
            self.tempo,
            self.loudness
        ], dtype=np.float64)

    def __repr__(self: "Song") -> str:
        return (f"Song(name={self.name}, track_id={self.track_id}, "
                f"danceability={self.danceability}, energy={self.energy}, "
                f"valence={self.valence})")

    def __str__(self: "Song") -> str:
        return f"'{self.name}' by {self.artists}"
