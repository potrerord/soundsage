from Data.Song import Song
from RecommendationSystem.Recommender import Recommender
from UserProfileSystem import UserProfile
import numpy as np
from numpy.typing import NDArray


class CosineSimilarity(Recommender):
    DEFAULT_TOP_N: int = 5

    user_profile: UserProfile
    all_songs: list[Song]
    top_n: int

    def __init__(
            self: "CosineSimilarity",
            user_profile: UserProfile,
            all_songs: list[Song],
            top_n: int = DEFAULT_TOP_N,
    ) -> None:
        self.user_profile = user_profile
        self.all_songs = all_songs
        self.top_n = top_n

    def _get_user_vector(
            self: "CosineSimilarity",
    ) -> NDArray[np.float64]:
        """
        Converts the user's profile into a vector for cosine similarity calculation.
        """
        return np.array([self.user_profile.danceability,
                         self.user_profile.energy,
                         self.user_profile.valence,
                         self.user_profile.acousticness,
                         self.user_profile.tempo,
                         self.user_profile.loudness,
                         ], dtype=np.float64)

    def calculate_cosine_similarity(
            self: "CosineSimilarity",
            user_vector: NDArray[np.floating],
            song_vector: NDArray[np.floating],
    ) -> np.floating:
        """
        Calculate cosine similarity between two vectors.
        """
        dot_product: np.floating = np.dot(user_vector, song_vector)
        magnitude_user: np.floating = np.linalg.norm(user_vector)
        magnitude_song: np.floating = np.linalg.norm(song_vector)

        # Add small epsilon to avoid division by zero
        epsilon: float = 1e-10
        cosine_similarity: np.floating = dot_product / (magnitude_user * magnitude_song + epsilon)
        return cosine_similarity

    def _get_all_cosine_similarity(
            self: "CosineSimilarity",
            user_vector: NDArray[np.floating],
            song_vectors: list[
                NDArray[np.floating]
            ],
    ) -> NDArray[np.floating]:
        """
        Vectorized computation of cosine similarity for multiple song vectors.
        """

        # Convert list of vectors to a NumPy matrix
        song_matrix: NDArray[np.floating] = np.array(song_vectors)

        # Compute dot products
        dot_products: NDArray[np.floating] = np.dot(song_matrix, user_vector)

        user_magnitude: np.floating = np.linalg.norm(user_vector)
        song_magnitudes: np.floating = np.linalg.norm(song_matrix, axis=1)  # Magnitudes for each song vector

        # Compute cosine similarities and avoid division by zero
        epsilon: float = 1e-10
        cosine_similarities: NDArray[np.floating] = dot_products / (user_magnitude * song_magnitudes + epsilon)

        return cosine_similarities

    def recommend(self: "CosineSimilarity") -> list[Song]:
        """
        Recommends songs based on cosine similarity between the user's profile and the songs.
        """
        user_vector: NDArray[np.floating] = self._get_user_vector()

        song_vectors: list[NDArray[np.floating]] = [song.to_vector() for song in self.all_songs]

        # Using native cosine similarities calculator for cosine similarities
        similarities: NDArray[np.floating] = (
            self._get_all_cosine_similarity(user_vector, song_vectors)
        )

        # Create a list of tuples (similarity_score, song_vector)
        similarity: float
        song: Song
        similarity_song_pairs: list[
            tuple[float, Song]
        ] = [(similarity, song) for similarity, song in zip(similarities, self.all_songs)]

        # Sort the list by similarity score (descending order)
        sorted_similarity_song_pairs: list[tuple[float, Song]] = (
            sorted(similarity_song_pairs, key=lambda pair: pair[0], reverse=True)
        )

        # Extract the top N recommended songs based on sorted similarity scores
        recommended_songs: list[Song] = [pair[1] for pair in sorted_similarity_song_pairs[:self.top_n]]

        print("Recommended songs from cosine similarity:")
        print([str(song) for song in recommended_songs])

        return recommended_songs
