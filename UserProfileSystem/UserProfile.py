import csv
from collections import Counter
import json
from statistics import mean
from typing import List, Optional
from Data.Song import Song
import numpy as np
import os
import Data.constants as c


class UserProfile:
    DEFAULT_TOP_N: int = 5

    user_id: str

    acousticness: float
    danceability: float
    energy: float
    instrumentalness: float
    liveness: float
    loudness: float
    popularity: float
    speechiness: float
    tempo: float
    valence: float

    key_counts: Counter[int]
    mode_counts: Counter[int]
    
    explicit_ratio: float
    explicit_tracks: int
    
    most_common_key: int
    most_common_mode: int

    # XXX are genre and artists represented by strings?
    # genres: Counter[str]
    artists: Counter[str]
    # popular_tracks: Counter[Song]

    song_count: int

    def __init__(
            self: "UserProfile",
            user_id: str,
    ) -> None:
        self.user_id = user_id

        # Aggregate numerical features
        self.acousticness = 0.0
        self.danceability = 0.0
        self.energy = 0.0
        self.instrumentalness = 0.0
        self.liveness = 0.0
        self.loudness = 0.0
        self.popularity = 0.0
        self.speechiness = 0.0
        self.tempo = 0.0
        self.valence = 0.0
        self.most_common_key = -1
        self.most_common_mode = -1
        self.explicit_ratio = -1
        self.explicit_tracks = -1
        # Aggregate categorical and textual features
        # self.genres = Counter()
        self.artists = Counter()
        # self.popular_tracks = Counter()

        # Count total songs processed for averaging
        self.song_count = 0

    def __repr__(self: "UserProfile") -> str:
        return (f"UserProfile(danceability={self.danceability:.2f}, energy={self.energy:.2f}, "
                f"valence={self.valence:.2f}, acousticness={self.acousticness:.2f}, "
                f"tempo={self.tempo:.2f}, loudness={self.loudness:.2f}, "
                f"top_artists={self.get_top_artists()})")

    def __str__(self: "UserProfile") -> str:
        return (
            f"UserProfile ID #{self.user_id} {{\n"
            f"    Song count: {self.song_count}\n"
            f"    Aggregated numerical features:\n"
            f"        Acousticness:     {self.acousticness:10.4f}\n"
            f"        Danceability:     {self.danceability:10.4f}\n"
            f"        Energy:           {self.energy:10.4f}\n"
            f"        Instrumentalness: {self.instrumentalness:10.4f}\n"
            f"        Liveness:         {self.liveness:10.4f}\n"
            f"        Loudness:         {self.loudness:10.4f}\n"
            f"        Popularity:       {self.popularity:10.4f}\n"
            f"        Speechiness:      {self.speechiness:10.4f}\n"
            f"        Tempo:            {self.tempo:10.4f}\n"
            f"        Valence:          {self.valence:10.4f}\n"
            f"\n"
            f"        Most common key:         {self.most_common_key}\n"
            f"        Most common mode:        {self.most_common_mode}\n"
            f"        Explicit song ratio:     {self.explicit_ratio:6.4f}\n"
            f"    Aggregated categorical and textual features:\n"
            f"        Top {self.DEFAULT_TOP_N} Artists: {self.get_top_artists()}\n"
            f"}}"
        )
    @staticmethod
    def create_profile_from_json(user_id: str, user_profiles_json: str) -> Optional["UserProfile"]:
        """
        Create a user profile from the existing JSON file if available.

        :param user_id: The user ID to look up in the JSON file.
        :param user_profiles_json: Path to the JSON file containing user profiles.
        :return: A UserProfile object if the user ID is found, otherwise None.
        """
        if os.path.exists(user_profiles_json):
            with open(user_profiles_json, 'r') as file:
                user_profiles = json.load(file)  # Load as a list of dictionaries
                print(user_profiles)  # Debug statement to inspect the loaded data
                
                # Find the user profile in the list by matching user_id
                for user_data in user_profiles:
                    if user_data.get("user_id") == user_id:
                        user_profile = UserProfile(user_id)
                        user_profile.acousticness = user_data.get('acousticness', 0.0)
                        user_profile.danceability = user_data.get('danceability', 0.0)
                        user_profile.energy = user_data.get('energy', 0.0)
                        user_profile.valence = user_data.get('valence', 0.0)
                        user_profile.tempo = user_data.get('tempo', 0.0)
                        user_profile.loudness = user_data.get('loudness', 0.0)
                        user_profile.genres = Counter(user_data.get('genres', {}))
                        user_profile.artists = Counter(user_data.get('artists', {}))
                        user_profile.popular_tracks = Counter(user_data.get('popular_tracks', {}))
                        user_profile.song_count = user_data.get('song_count', 0)
                        return user_profile

        return None
    
    @staticmethod
    def create_profile_from_songs_csv(
            user_id: str,
            songs_csv: str,
            user_profiles_json: str
    ) -> "UserProfile":
        user_profile = UserProfile.create_profile_from_json(user_id, user_profiles_json)
        if user_profile:
            print(f"Profile for user {user_id} loaded from JSON.")
            return user_profile
        
        print(f"\nCreating user profile from {songs_csv}...")
        
        new_user_profile = UserProfile(user_id)

        # Read the CSV and process each row
        with open(songs_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse numerical features and construct a Song object
                song = Song(
                    id=row["id"],
                    name=row["name"],
                    album=row["album"],
                    album_id=None,  # Album ID not present in CSV
                    artists=row["artists"].split(", "),  # Assumes multiple artists are comma-separated
                    artist_ids=None,  # Artist IDs not present in CSV
                    track_number=None,  # Track number not present in CSV
                    disc_number=None,  # Disc number not present in CSV
                    explicit=row["explicit"].lower() == "true",
                    danceability=float(row["danceability"]),
                    energy=float(row["energy"]),
                    key=int(row["key"]),
                    loudness=float(row["loudness"]),
                    mode=int(row["mode"]),
                    speechiness=float(row["speechiness"]),
                    acousticness=float(row["acousticness"]),
                    instrumentalness=float(row["instrumentalness"]),
                    liveness=float(row["liveness"]),
                    valence=float(row["valence"]),
                    tempo=float(row["tempo"]),
                    duration_ms=int(row["duration_ms"]),
                    time_signature=int(row["time_signature"]),
                    year=None,  # Year not present in CSV
                    release_date=None,  # Release date not present in CSV
                    popularity=float(row["popularity"]),
                )

                # Update the profile with this song's data
                new_user_profile.update_profile_with_song(song)

        return new_user_profile

    def update_profile_with_song(
            self: "UserProfile",
            song: Song,
    ) -> None:
        """Update the user profile with a single Song instance.
        
        Parameters:
            song (Song): The Song that will update the user profile.
        """

        # Update aggregate numerical features
        self.danceability = ((self.danceability * self.song_count) + song.danceability) / (self.song_count + 1)
        self.energy = ((self.energy * self.song_count) + song.energy) / (self.song_count + 1)
        self.valence = ((self.valence * self.song_count) + song.valence) / (self.song_count + 1)
        self.acousticness = ((self.acousticness * self.song_count) + song.acousticness) / (self.song_count + 1)
        self.tempo = ((self.tempo * self.song_count) + song.tempo) / (self.song_count + 1)
        self.loudness = ((self.loudness * self.song_count) + song.loudness) / (self.song_count + 1)
        self.speechiness = ((self.speechiness * self.song_count) + song.speechiness) / (self.song_count + 1)
        self.instrumentalness = ((self.instrumentalness * self.song_count) + song.instrumentalness) / (
                    self.song_count + 1)
        self.liveness = ((self.liveness * self.song_count) + song.liveness) / (self.song_count + 1)

        # Track most common categorical features
        # self.genres.update(song.genres)  # Aggregate genres
        self.artists.update(song.artists)  # Aggregate artist counts

        # Handle "key" and "mode" as most common values
        if not hasattr(self, "key_counts"):
            self.key_counts = Counter()
        if not hasattr(self, "mode_counts"):
            self.mode_counts = Counter()

        self.key_counts[song.key] += 1
        self.mode_counts[song.mode] += 1

        self.most_common_key = self.key_counts.most_common(1)[0][0]  # Track most common key
        self.most_common_mode = self.mode_counts.most_common(1)[0][0]  # Track most common mode

        # Calculate the ratio of explicit songs
        explicit_tracks = getattr(self, "explicit_tracks", 0) + (1 if song.explicit else 0)
        self.explicit_ratio = explicit_tracks / (self.song_count + 1)
        self.explicit_tracks = explicit_tracks  # Track explicit count for future updates

        # Track popularity as an average
        if hasattr(self, "popularity"):
            self.popularity = ((self.popularity * self.song_count) + song.popularity) / (self.song_count + 1)
        else:
            self.popularity = song.popularity

        # Increment song count
        self.song_count += 1

    def update_profile_with_songs(
            self: "UserProfile",
            songs: list[Song],
    ) -> None:
        """
        Updates the user profile with a collection of Song instances.
        """
        song: Song
        for song in songs:
            print(f"\nUpdating user profile for {song.id}...")
            self.update_profile_with_song(song)
            print(f"New user profile: {self}")

    # def get_top_genres(
    #         self: "UserProfile",
    #         n: int = DEFAULT_TOP_N,
    # ) -> list[tuple[str, int]]:
    #     """Returns the top N genres by frequency."""
    # 
    #     return self.genres.most_common(n)

    def get_top_artists(
            self: "UserProfile",
            n: int = DEFAULT_TOP_N,
    ) -> list[tuple[str, int]]:
        """Returns the top N artists by frequency."""

        return self.artists.most_common(n)

    # def get_favorite_tracks(
    #         self: "UserProfile",
    #         n: int = DEFAULT_TOP_N,
    # ) -> list[tuple[Song, int]]:
    #     """Returns the user's most frequently listened tracks."""
    # 
    #     return self.popular_tracks.most_common(n)

    def get_user_vector(
            self: "UserProfile",
            top_n: int = DEFAULT_TOP_N,
    ) -> np.ndarray[np.shape, np.dtype[np.floating]]:
        """
        Converts the user's profile into a numerical vector representation.
        
        Returns a vector of:
        - Average numerical features (danceability, energy, etc.)
        - One-hot encoded vector for top N genres and artists
        """
        # Numerical features
        numerical_features: np.ndarray[
            np.shape,
            np.dtype[np.floating]
        ] = np.array([
            self.danceability,
            self.energy,
            self.valence,
            self.acousticness,
            self.tempo,
            self.loudness,
        ])

        # Get the top N genres and artists
        # top_genres: list[tuple[str, int]] = self.get_top_genres(top_n)
        top_artists: list[tuple[str, int]] = self.get_top_artists(top_n)

        # One-hot encoding (or simple frequency count) for top N genres and artists
        # genre_vector: np.ndarray[
        #     np.shape,
        #     np.dtype[np.floating]
        # ] = np.zeros(top_n)  # One-hot vector for top N genres

        artist_vector: np.ndarray[
            np.shape,
            np.dtype[np.floating]
        ] = np.zeros(top_n)  # One-hot vector for top N artists

        # i: int
        # genre: str
        # for i, (genre, _) in enumerate(top_genres):
        #     genre_vector[i] = 1  # Mark the genre as present

        artist: str
        for i, (artist, _) in enumerate(top_artists):
            artist_vector[i] = 1  # Mark the artist as present

        # Combine all features into a single vector
        user_vector: np.ndarray[
            np.shape,
            np.dtype[np.floating]
        ] = np.concatenate([numerical_features, artist_vector])

        return user_vector

    def is_cold_start(self: "UserProfile") -> bool:
        """
        Checks if the user profile is a cold start.
        
        :return: True if the profile is a cold start, False otherwise.
        """
        # If no songs have been processed, or no meaningful data in the profile, it's a cold start
        return (self.song_count == 0
                and all(val == 0.0 for val in [
                    self.danceability,
                    self.energy,
                    self.valence,
                    self.acousticness,
                    self.tempo,
                    self.loudness
                ])
                # and not self.genres
                and not self.artists)

    def validate_features(
            self: "UserProfile",
    ) -> None:
        if not (c.ACOUSTICNESS_MIN <= self.acousticness <= c.ACOUSTICNESS_MAX):
            raise ValueError(
                f"invalid user acousticness: {self.acousticness:.4f} not in range [{c.ACOUSTICNESS_MIN}, {c.ACOUSTICNESS_MAX}].")

        if not (c.DANCEABILITY_MIN <= self.danceability <= c.DANCEABILITY_MAX):
            raise ValueError(
                f"invalid user danceability: {self.danceability:.4f} not in range [{c.DANCEABILITY_MIN}, {c.DANCEABILITY_MAX}].")

        if not (c.ENERGY_MIN <= self.energy <= c.ENERGY_MAX):
            raise ValueError(f"invalid user energy: {self.energy:.4f} not in range [{c.ENERGY_MIN}, {c.ENERGY_MAX}].")

        if not (c.LOUDNESS_MIN_USEFUL <= self.loudness <= c.LOUDNESS_MAX):
            raise ValueError(
                f"invalid user loudness: {self.loudness:.4f} not in range [{c.LOUDNESS_MIN_USEFUL}, {c.LOUDNESS_MAX}].")

        if not (c.TEMPO_MIN_USEFUL <= self.tempo <= c.TEMPO_MAX_USEFUL):
            raise ValueError(
                f"invalid user tempo: {self.tempo:.4f} not in range [{c.TEMPO_MIN_USEFUL}, {c.TEMPO_MAX_USEFUL}].")

        if not (c.VALENCE_MIN <= self.valence <= c.VALENCE_MAX):
            raise ValueError(
                f"invalid user valence: {self.valence:.4f} not in range [{c.VALENCE_MIN}, {c.VALENCE_MAX}].")

        # TODO add more
        # speechiness: float
