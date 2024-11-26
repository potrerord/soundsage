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
            release_date: str,
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

        # Ensure that the song data is valid.
        self.validate_features()

    def __repr__(self: "Song") -> str:
        return (f"Song(name={self.name}, track_id={self.track_id}, "
                f"danceability={self.danceability}, energy={self.energy}, "
                f"valence={self.valence})")

    def __str__(self: "Song") -> str:
        return f"'{self.name}' by {self.artists}"

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

    def validate_features(
            self: "Song",
    ) -> None:
        if not (c.ACOUSTICNESS_MIN <= self.acousticness <= c.ACOUSTICNESS_MAX):
            raise ValueError(f"invalid song acousticness: {self.acousticness:.4f} not in range [{c.ACOUSTICNESS_MIN}, {c.ACOUSTICNESS_MAX}].")

        if not (c.DANCEABILITY_MIN <= self.danceability <= c.DANCEABILITY_MAX):
            raise ValueError(f"invalid song danceability: {self.danceability:.4f} not in range [{c.DANCEABILITY_MIN}, {c.DANCEABILITY_MAX}].")

        if not (c.ENERGY_MIN <= self.energy <= c.ENERGY_MAX):
            raise ValueError(f"invalid song energy: {self.energy:.4f} not in range [{c.ENERGY_MIN}, {c.ENERGY_MAX}].")

        if not (c.INSTRUMENTALNESS_MIN <= self.instrumentalness <= c.INSTRUMENTALNESS_MAX):
            raise ValueError(f"invalid song instrumentalness: {self.instrumentalness:.4f} not in range [{c.INSTRUMENTALNESS_MIN}, {c.INSTRUMENTALNESS_MAX}].")

        if not ((c.KEY_MIN <= self.key <= c.KEY_MAX) or (self.key == c.KEY_NONE_DETECTED)):
            raise ValueError(f"invalid song key: {self.key:.4f} not in range [{c.KEY_MIN}, {c.KEY_MAX}].")
        
        if not (c.LIVENESS_MIN <= self.liveness <= c.LIVENESS_MAX):
            raise ValueError(f"invalid song liveness: {self.liveness:.4f} not in range [{c.LIVENESS_MIN}, {c.LIVENESS_MAX}].")

        if not (c.LOUDNESS_MIN_USEFUL <= self.loudness <= c.LOUDNESS_MAX):
            raise ValueError(f"invalid song loudness: {self.loudness:.4f} not in range [{c.LOUDNESS_MIN_USEFUL}, {c.LOUDNESS_MAX}].")
        
        if not (self.mode == c.MODE_MINOR or self.mode == c.MODE_MAJOR):
            raise ValueError(f"invalid song mode: {self.mode:.4f} not in range [{c.MODE_MINOR}, {c.MODE_MAJOR}].")
        
        if not (c.SPEECHINESS_MIN <= self.speechiness <= c.SPEECHINESS_MAX):
            raise ValueError(f"invalid song speechiness: {self.speechiness:.4f} not in range {c.SPEECHINESS_MIN}, {c.SPEECHINESS_MAX}].")
        
        if not (c.TEMPO_MIN_USEFUL <= self.tempo <= c.TEMPO_MAX_USEFUL):
            raise ValueError(f"invalid song tempo: {self.tempo:.4f} not in range [{c.TEMPO_MIN_USEFUL}, {c.TEMPO_MAX_USEFUL}].")
        
        if not (c.TIME_SIG_MIN <= self.time_signature <= c.TIME_SIG_MAX):
            raise ValueError(f"invalid song time_signature: {self.time_signature:.4f} not in range [{c.TIME_SIG_MIN}, {c.TIME_SIG_MAX}].")
        
        if not (c.VALENCE_MIN <= self.valence <= c.VALENCE_MAX):
            raise ValueError(f"invalid song valence: {self.valence:.4f} not in range [{c.VALENCE_MIN}, {c.VALENCE_MAX}].")
