import numpy as np
from Data.Song import Song
from RecommendationSystem.Recommender import Recommender
from UserProfileSystem.UserProfile import UserProfile

from numpy.typing import NDArray


class KNNRecommender(Recommender):
    """A recommender class that uses a UserProfile and a list of songs
    to recommend a new list of songs based on an K-nearest neighbors
    machine learning approach.
    """

    # The default number of nearest neighbors to explore.
    DEFAULT_K: int = 5

    # The default number of songs to recommend.
    DEFAULT_TOP_N: int = 10

    # The features utilized by this recommender.
    FEATURE_COLUMNS: list[str] = [
        "acousticness",
        "danceability",
        "energy",
        "key",
        "instrumentalness",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "valence",
    ]

    # A default value for a "null" feature.
    EMPTY_FEATURE_VALUE: float = 0.0

    # The user profile containing data used for recommendations.
    user_profile: UserProfile

    # The songs used to compute the recommendations.
    all_songs: list[Song]

    # The number of nearest neighbors to explore.
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
                The number of nearest neighbors to explore.
        """

        self.user_profile = user_profile
        self.all_songs = all_songs
        self.k = k

    def recommend(
            self: "KNNRecommender",
            top_n: int = DEFAULT_TOP_N,
    ) -> list[Song]:
        """Recommend a list of songs based on the Euclidean distance
        between the user profile vector and each song vector, picking
        the top n most similar songs from the k nearest neighbors.
        
        Parameters:
            top_n (int): The number of songs to recommend.
        
        Returns:
            A list of Song objects.
        """
        
        print(f"\nGetting KNN recommendations for {self.user_profile}...")

        # Get the user profile vector.
        user_vector: NDArray[np.floating] = self._get_user_vector()

        # Calculate distances from user vector to all songs.
        distances: list[tuple[Song, np.floating]] = []
        song: Song
        for song in self.all_songs:
            song_vector: NDArray[np.floating] = self._get_song_vector(song)
            distance: np.floating = self._euclidean_distance(user_vector, song_vector)
            distances.append((song, distance))

        # Sort by distance (ascending order).
        distances.sort(key=lambda x: x[1])

        # Select the top k neighbors.
        nearest_neighbors: list[tuple[Song, np.floating]] = distances[:self.k]

        # Aggregate and return top n recommendations based on nearest neighbors.
        recommended_songs: list[Song] = [song for (song, _) in nearest_neighbors][:top_n]

        # Print recommended songs.
        print("Recommended songs from KNN: [")
        i: int = 0
        for song in recommended_songs:
            print(f"    ({i}) {song}")
            i += 1
        print("]")

        return recommended_songs

    def _get_user_vector(self: "KNNRecommender") -> NDArray[np.floating]:
        """Create a feature vector by averaging features of the user's 
        liked songs.
        
        Returns:
            A feature vector.
        """

        liked_songs: list[tuple[Song, int]] = self.user_profile.get_favorite_tracks()
        if not liked_songs:
            return np.zeros(len(self.FEATURE_COLUMNS))  # Handle cold start

        song: Song
        vectors = [self._get_song_vector(song) for (song, _) in liked_songs]

        return np.mean(vectors, axis=0)

    def _get_song_vector(
            self: "KNNRecommender",
            song: Song,
    ) -> NDArray[np.floating]:
        """Convert a song's features into a numeric vector.
        
        Parameters:
            song (Song): The song to convert.
            
        Returns:
            A numeric vector of the song's features.
        """

        feature_name: str
        return np.array(
            [getattr(song, feature_name, self.EMPTY_FEATURE_VALUE) for feature_name in self.FEATURE_COLUMNS],
            dtype=float)

    @staticmethod
    def _euclidean_distance(
            vec1: NDArray[np.floating],
            vec2: NDArray[np.floating],
    ) -> np.floating:
        """Compute the Euclidean distance between two vectors.
        
        Parameters:
            vec1 (NDArray[np.floating]): The first vector.
            vec2 (NDArray[np.floating]): The second vector.
        
        Returns:
            The Euclidean distance between the two vectors.
        """

        return np.sqrt(np.sum((vec1 - vec2) ** 2))
