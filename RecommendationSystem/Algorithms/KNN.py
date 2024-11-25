import numpy as np
from Data.Song import Song
from RecommendationSystem.Recommender import Recommender
from UserProfileSystem.UserProfile import UserProfile


class KNNRecommender(Recommender):
    DEFAULT_K: int = 5

    FEATURE_COLUMNS: list[str] = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    ]

    user_profile: UserProfile
    all_songs: list[Song]
    k: int

    def __init__(
            self: "KNNRecommender",
            user_profile: UserProfile,
            all_songs: list[Song],
            k: int = DEFAULT_K,
    ) -> None:
        """Instantiate and initialize a KNN recommender.
        
        Parameters:
            user_profile (UserProfile):
                The user profile that will be used to compute the
                recommendations.
            all_songs (list[Song]):
                The songs that will be used to compute the
                recommendations.
            k (int):
                The number of neighbors to use.
        """

        self.user_profile = user_profile
        self.all_songs = all_songs
        self.k = k  # Number of neighbors to consider

    def recommend(
            self: "KNNRecommender",
            top_n: int = 10,
    ) -> list[Song]:
        """Recommend a list of songs based on the Euclidean distance
        between the user profile vector and each song vector, picking
        the top n most similar songs from the k nearest neighbors.
        
        Parameters:
            top_n (int): The number of songs to recommend.
        
        Returns:
            A list of Song objects.
        """

        # Get the user profile vector.
        user_vector: np.ndarray = self._get_user_vector()

        # Calculate distances from user vector to all songs.
        distances: list[tuple[Song, float]] = []
        song: Song
        for song in self.all_songs:
            song_vector = self._get_song_vector(song)
            distance = self._euclidean_distance(user_vector, song_vector)
            distances.append((song, distance))

        # Sort by distance (ascending order).
        distances.sort(key=lambda x: x[1])

        # Select the top k neighbors.
        nearest_neighbors = distances[:self.k]

        # Aggregate and return top n recommendations based on nearest neighbors.
        recommended_songs = [song for song, _ in nearest_neighbors][:top_n]

        return recommended_songs

    def _get_user_vector(self: "KNNRecommender") -> np.ndarray:
        """Create a feature vector by averaging features of the user's 
        liked songs.
        
        Returns:
            A feature vector.
        """

        liked_songs = self.user_profile.get_favorite_tracks()
        if not liked_songs:
            return np.zeros(len(self.FEATURE_COLUMNS))  # Handle cold start

        vectors = [self._get_song_vector(song) for song in liked_songs]

        return np.mean(vectors, axis=0)

    def _get_song_vector(
            self: "KNNRecommender",
            song: Song,
    ) -> np.ndarray:
        """Convert a song's features into a numeric vector.
        
        Parameters:
            song (Song): The song to convert.
            
        Returns:
            A numeric vector.
        """

        return np.array([getattr(song, col, 0.0) for col in self.FEATURE_COLUMNS], dtype=float)

    def _euclidean_distance(
            self: "KNNRecommender",
            vec1: np.ndarray,
            vec2: np.ndarray,
    ) -> float:
        """Compute the Euclidean distance between two vectors.
        
        Parameters:
            vec1 (np.ndarray): The first vector.
            vec2 (np.ndarray): The second vector.
        
        Returns:
            The Euclidean distance between the two vectors.
        """

        return np.sqrt(np.sum((vec1 - vec2) ** 2))
