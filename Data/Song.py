from collections import Counter

import numpy as np
from numpy.typing import NDArray

import Data.constants as c


class Song:
    """A representation of a complete set of Spotify song data."""
    
    id: str | None
    name: str | None
    album: str | None
    album_id: str | None
    artists: list[str] | None
    artist_ids: list[str] | None
    track_number: int | None
    disc_number: int | None
    explicit: bool | None
    danceability: float | None
    energy: float | None
    key: int | None
    loudness: float | None
    mode: int | None
    speechiness: float | None
    acousticness: float | None
    instrumentalness: float | None
    liveness: float | None
    valence: float | None
    tempo: float | None
    duration_ms: int | None
    time_signature: float | None
    year: int | None
    release_date: str | None
    genres: Counter[str] | None

    def __init__(
            self,
            id: str | None,
            name: str | None,
            album: str | None,
            album_id: str | None,
            artists: list[str] | None,
            artist_ids: list[str] | None,
            track_number: int | None,
            disc_number: int | None,
            explicit: bool | None,
            danceability: float | None,
            energy: float | None,
            key: int | None,
            loudness: float | None,
            mode: int | None,
            speechiness: float | None,
            acousticness: float | None,
            instrumentalness: float | None,
            liveness: float | None,
            valence: float | None,
            tempo: float | None,
            duration_ms: int | None,
            time_signature: float | None,
            year: int | None,
            release_date: str | None,
            popularity: float | None,
    ) -> None:
        """Initialize a Song object.
        
        Parameters:
            id (str): The track ID.
            name (str): The song name.
            album (str): The album.
            album_id (str): The album ID.
            artists (list[str]): A list of artists credited on the song.
            artist_ids (list[str]): The list of respective artist IDs.
            track_number (int): The track number.
            disc_number (int): The disc number.
            explicit (bool): Whether the song is explicit or not.
            danceability (float): The danceability value of the song.
            energy (float): The energy value of the song.
            key (int): The encoded key of the song .
            loudness (float): The loudness of the song in dBFS.
            mode (int): The mode of the song (major/minor).
            speechiness (float): A measure of the amount of speech the song contains.
            acousticness (float): A measure of how acoustic the song is.
            instrumentalness (float): A measure of how instrumental the song is.
            liveness (float): A measure of how live the song is.
            valence (float): A measure of the song's positivity.
            tempo (float): The tempo of the song in beats per minute.
            duration_ms (int): The duration of the song in milliseconds.
            time_signature (float): The encoded time signature of the song.
            year (int): The year of the song's release.
            release_date (str): The complete release date of the song.
            popularity (float): The popularity of the song.
        """

        self.id = id
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
        self.popularity = popularity
        
        # Ensure that the song data is valid.
        self.validate_features()

    def __repr__(self: "Song") -> str:
        return (f"Song(name={self.name}, id={self.id}, "
                f"danceability={self.danceability}, energy={self.energy}, "
                f"valence={self.valence})")

    def __str__(self: "Song") -> str:
        return f"'{self.name}' by {self.artists}"

    def to_vector(self: "Song") -> NDArray[np.float64]:
        """Convert the song's features into a numerical vector for
        cosine similarity calculation.
        
        Returns:
            A vector representing the song's features.
        """

        return np.array([
            self.acousticness,
            self.danceability,
            self.energy,
            self.loudness,
            self.tempo,  # FIXME - tempo is not a good feature to weigh heavily
            self.valence,
        ], dtype=np.float64)

    def validate_features(
            self: "Song",
    ) -> None:
        """Check that each of the song's features falls within its
        respective valid range of values.
        
        Raises:
            ValueError: If any of the features do not fall within their acceptable ranges.
        """

        if not (c.ACOUSTICNESS_MIN <= self.acousticness <= c.ACOUSTICNESS_MAX):
            raise ValueError(
                f"invalid song acousticness: {self.acousticness:.4f} not in range [{c.ACOUSTICNESS_MIN}, {c.ACOUSTICNESS_MAX}]."
            )

        if not (c.DANCEABILITY_MIN <= self.danceability <= c.DANCEABILITY_MAX):
            raise ValueError(
                f"invalid song danceability: {self.danceability:.4f} not in range [{c.DANCEABILITY_MIN}, {c.DANCEABILITY_MAX}]."
            )

        if not (c.ENERGY_MIN <= self.energy <= c.ENERGY_MAX):
            raise ValueError(f"invalid song energy: {self.energy:.4f} not in range [{c.ENERGY_MIN}, {c.ENERGY_MAX}]."
                             )

        if not (c.INSTRUMENTALNESS_MIN <= self.instrumentalness <= c.INSTRUMENTALNESS_MAX):
            raise ValueError(
                f"invalid song instrumentalness: {self.instrumentalness:.4f} not in range [{c.INSTRUMENTALNESS_MIN}, {c.INSTRUMENTALNESS_MAX}]."
            )

        if not ((c.KEY_MIN <= self.key <= c.KEY_MAX) or (self.key == c.KEY_NONE_DETECTED)):
            raise ValueError(
                f"invalid song key: {self.key:.4f} not in range [{c.KEY_MIN}, {c.KEY_MAX}]."
            )

        if not (c.LIVENESS_MIN <= self.liveness <= c.LIVENESS_MAX):
            raise ValueError(
                f"invalid song liveness: {self.liveness:.4f} not in range [{c.LIVENESS_MIN}, {c.LIVENESS_MAX}]."
            )

        if not (c.LOUDNESS_MIN_USEFUL <= self.loudness <= c.LOUDNESS_MAX):
            raise ValueError(
                f"invalid song loudness: {self.loudness:.4f} not in range [{c.LOUDNESS_MIN_USEFUL}, {c.LOUDNESS_MAX}]."
            )

        if not (self.mode == c.MODE_MINOR or self.mode == c.MODE_MAJOR):
            raise ValueError(
                f"invalid song mode: {self.mode:.4f} not in range [{c.MODE_MINOR}, {c.MODE_MAJOR}]."
            )

        if not (c.SPEECHINESS_MIN <= self.speechiness <= c.SPEECHINESS_MAX):
            raise ValueError(
                f"invalid song speechiness: {self.speechiness:.4f} not in range {c.SPEECHINESS_MIN}, {c.SPEECHINESS_MAX}]."
            )

        if not (c.TEMPO_MIN_USEFUL <= self.tempo <= c.TEMPO_MAX_USEFUL):
            raise ValueError(
                f"invalid song tempo: {self.tempo:.4f} not in range [{c.TEMPO_MIN_USEFUL}, {c.TEMPO_MAX_USEFUL}]."
            )

        if not (c.TIME_SIG_MIN <= self.time_signature <= c.TIME_SIG_MAX):
            raise ValueError(
                f"invalid song time_signature: {self.time_signature:.4f} not in range [{c.TIME_SIG_MIN}, {c.TIME_SIG_MAX}]."
            )

        if not (c.VALENCE_MIN <= self.valence <= c.VALENCE_MAX):
            raise ValueError(
                f"invalid song valence: {self.valence:.4f} not in range [{c.VALENCE_MIN}, {c.VALENCE_MAX}]."
            )
