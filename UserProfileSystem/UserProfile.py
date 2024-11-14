from collections import Counter
from statistics import mean
from typing import List
from Data import Song

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
    
    def __repr__(self):
        return (f"UserProfile(danceability={self.danceability:.2f}, energy={self.energy:.2f}, "
                f"valence={self.valence:.2f}, acousticness={self.acousticness:.2f}, "
                f"tempo={self.tempo:.2f}, loudness={self.loudness:.2f}, "
                f"top_genres={self.get_top_genres()}, top_artists={self.get_top_artists()})")