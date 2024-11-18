from typing import List
from Data.Song import Song
from RecommendationSystem import Recommender
from UserProfileSystem import UserProfile
import numpy as np

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
    
    def calculate_cosine_similarity(self, user_vector, song_vector): 
        '''
        Calculate individual cosine similarity
        '''
        # Calculate dot product
        dot_product = np.dot(user_vector, song_vector)
        # Calculate the magnitude of each vector
        magnitude_user = np.linalg.norm(user_vector)
        magnitude_song = np.linalg.norm(song_vector)

        # Compute cosine similarity
        cosine_similarity = dot_product / (magnitude_user * magnitude_song)
        return cosine_similarity
    
    def get_all_cosine_similarity(self, user_vector, song_vectors): 
        '''
        Compile all cosine similarity 
        '''
        similarities = np.array([])
        for vector in song_vectors: 
            similarity = self.calculate_cosine_similarity(user_vector, vector)
            np.append(similarities, similarity)
        return similarities

    def recommend(self) -> List[Song]:
        """
        Recommends songs based on cosine similarity between the user's profile and the songs.
        """
        user_vector = self.get_user_vector()
        song_vectors = [song.to_vector() for song in self.all_songs]
        
        # Using native cosine similarities calculator for cosine similarities
        similarities = self.get_all_cosine_similarity(user_vector, song_vectors)
        
        # Sort songs by similarity (most similar songs first)
        sorted_song_indices = np.argsort(similarities)[::-1]
        
        # Get the top N recommended songs
        recommended_songs = [self.all_songs[i] for i in sorted_song_indices[:self.top_n]]
        
        print("recommended songs from cosine similarity")
        print(recommended_songs)

        return recommended_songs