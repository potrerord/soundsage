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
        """
        Calculate cosine similarity between two vectors.
        """
        dot_product = np.dot(user_vector, song_vector)
        magnitude_user = np.linalg.norm(user_vector)
        magnitude_song = np.linalg.norm(song_vector)

        # Add small epsilon to avoid division by zero
        epsilon = 1e-10
        cosine_similarity = dot_product / (magnitude_user * magnitude_song + epsilon)
        return cosine_similarity

    def _get_all_cosine_similarity(
            self: "CosineSimilarity",
            user_vector: np.ndarray,
            song_vectors: list[np.ndarray],
    ) -> np.ndarray:
        """
        Vectorized computation of cosine similarity for multiple song vectors.
        """
        song_matrix: np.ndarray = np.array(song_vectors)  # Convert list of vectors to a NumPy matrix
        dot_products: np.ndarray = np.dot(song_matrix, user_vector)  # Compute dot products
        user_magnitude: np.floating = np.linalg.norm(user_vector)
        song_magnitudes: np.floating = np.linalg.norm(song_matrix, axis=1)  # Magnitudes for each song vector

        # Compute cosine similarities and avoid division by zero
        epsilon: float = 1e-10
        cosine_similarities: np.ndarray = dot_products / (user_magnitude * song_magnitudes + epsilon)
        
        return cosine_similarities

    def recommend(self) -> list[Song]:
        """
        Recommends songs based on cosine similarity between the user's profile and the songs.
        """
        user_vector: np.ndarray = self.get_user_vector()
        song_vectors: list[np.ndarray] = [song.to_vector() for song in self.all_songs]

        # Using native cosine similarities calculator for cosine similarities
        similarities = self._get_all_cosine_similarity(user_vector, song_vectors)

        # Create a list of tuples (similarity_score, song_vector)
        similarity_song_pairs = [(similarity, song) for similarity, song in zip(similarities, self.all_songs)]

        # Sort the list by similarity score (descending order)
        sorted_similarity_song_pairs = sorted(similarity_song_pairs, key=lambda pair: pair[0], reverse=True)

        # Extract the top N recommended songs based on sorted similarity scores
        recommended_songs = [pair[1] for pair in sorted_similarity_song_pairs[:self.top_n]]

        print("Recommended songs from cosine similarity:")
        print(recommended_songs)

        return recommended_songs
