from collections import Counter
from statistics import mean
from typing import List
from Data import Song
import numpy as np

class UserProfile:
    def __init__(self, user_id: str):
        # Aggregate numerical features
        self.user_id = user_id
        self.danceability = 0.0
        self.energy = 0.0
        self.valence = 0.0
        self.acousticness = 0.0
        self.tempo = 0.0
        self.loudness = 0.0
        
        # Aggregate categorical and textual features
        self.genres = Counter()
        self.artists = Counter()
        self.popular_tracks = Counter()
        
        # Count total songs processed for averaging
        self.song_count = 0

    def update_profile_with_song(self, song: Song):
        """
        Updates the user profile with a single Song instance.
        """
        # Update aggregate numerical features
        self.danceability = ((self.danceability * self.song_count) + song.danceability) / (self.song_count + 1)
        self.energy = ((self.energy * self.song_count) + song.energy) / (self.song_count + 1)
        self.valence = ((self.valence * self.song_count) + song.valence) / (self.song_count + 1)
        self.acousticness = ((self.acousticness * self.song_count) + song.acousticness) / (self.song_count + 1)
        self.tempo = ((self.tempo * self.song_count) + song.tempo) / (self.song_count + 1)
        self.loudness = ((self.loudness * self.song_count) + song.loudness) / (self.song_count + 1)
        
        # Update categorical and textual features
        self.genres.update(song.genres)
        self.artists.update([song.artist])
        self.popular_tracks.update([song.track_id])
        
        # Increment song count
        self.song_count += 1

    def update_profile_with_songs(self, songs: List[Song]):
        """
        Updates the user profile with a collection of Song instances.
        """
        for song in songs:
            self.update_profile_with_song(song)

    def get_top_genres(self, n=5):
        """Returns the top N genres by frequency."""
        return self.genres.most_common(n)
    
    def get_top_artists(self, n=5):
        """Returns the top N artists by frequency."""
        return self.artists.most_common(n)

    def get_favorite_tracks(self, n=5):
        """Returns the user's most frequently listened tracks."""
        return self.popular_tracks.most_common(n)
    
    def get_user_vector(self, top_n=5) -> np.ndarray:
        """
        Converts the user's profile into a numerical vector representation.
        
        Returns a vector of:
        - Average numerical features (danceability, energy, etc.)
        - One-hot encoded vector for top N genres and artists
        """
        # Numerical features
        numerical_features = [
            self.danceability,
            self.energy,
            self.valence,
            self.acousticness,
            self.tempo,
            self.loudness
        ]
        
        # Get the top N genres and artists
        top_genres = self.get_top_genres(top_n)
        top_artists = self.get_top_artists(top_n)
        
        # One-hot encoding (or simple frequency count) for top N genres and artists
        genre_vector = np.zeros(top_n)  # One-hot vector for top N genres
        artist_vector = np.zeros(top_n)  # One-hot vector for top N artists
        
        for i, (genre, _) in enumerate(top_genres):
            genre_vector[i] = 1  # Mark the genre as present
        
        for i, (artist, _) in enumerate(top_artists):
            artist_vector[i] = 1  # Mark the artist as present
        
        # Combine all features into a single vector
        user_vector = np.concatenate([numerical_features, genre_vector, artist_vector])
        
        return user_vector

    def is_cold_start(self) -> bool:
        """
        Checks if the user profile is a cold start.
        
        :return: True if the profile is a cold start, False otherwise.
        """
        # If no songs have been processed, or no meaningful data in the profile, it's a cold start
        return self.song_count == 0 and all(val == 0.0 for val in [
            self.danceability,
            self.energy,
            self.valence,
            self.acousticness,
            self.tempo,
            self.loudness
        ]) and not self.genres and not self.artists
    
    def __repr__(self):
        return (f"UserProfile(danceability={self.danceability:.2f}, energy={self.energy:.2f}, "
                f"valence={self.valence:.2f}, acousticness={self.acousticness:.2f}, "
                f"tempo={self.tempo:.2f}, loudness={self.loudness:.2f}, "
                f"top_genres={self.get_top_genres()}, top_artists={self.get_top_artists()})")