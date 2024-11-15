from typing import List
from Data import Song
from RecommendationSystem import Recommender
from UserProfileSystem import UserProfile
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CosineSimilarity:
    def __init__(self, user_profile: UserProfile, all_songs: List[Song], top_n: int = 5):
        self.user_profile = user_profile
        self.all_songs = all_songs
        self.top_n = top_n

    def get_user_vector(self):
        """
        Converts the user's profile into a vector for cosine similarity calculation.
        """
        return np.array([
            self.user_profile.danceability,
            self.user_profile.energy,
            self.user_profile.valence,
            self.user_profile.acousticness,
            self.user_profile.tempo,
            self.user_profile.loudness
        ])

    def recommend(self) -> List[Song]:
        """
        Recommends songs based on cosine similarity between the user's profile and the songs.
        """
        user_vector = self.get_user_vector()
        song_vectors = [song.to_vector() for song in self.all_songs]
        
        # Calculate cosine similarities between the user profile vector and all song vectors
        similarities = cosine_similarity([user_vector], song_vectors)[0]
        
        # Sort songs by similarity (most similar songs first)
        sorted_song_indices = np.argsort(similarities)[::-1]
        
        # Get the top N recommended songs
        recommended_songs = [self.all_songs[i] for i in sorted_song_indices[:self.top_n]]
        
        print("recommended songs from cosine similarity")
        print(recommended_songs)

        return recommended_songs