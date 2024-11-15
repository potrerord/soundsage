from sklearn.neighbors import NearestNeighbors
import numpy as np
from typing import List
from Data import Song
from UserProfileSystem.UserProfile import UserProfile

class KNNRecommender:
    def __init__(self, user_profile: UserProfile, all_songs: List[Song], k: int = 5):
        """
        Initializes the KNN recommender using scikit-learn's NearestNeighbors.

        :param all_songs: List of all available Song objects.
        :param k: Number of nearest neighbors to consider.
        """
        self.user_profile = user_profile
        self.all_songs = all_songs
        self.k = k

        # Extract feature vectors from the songs
        self.song_features = np.array([song.to_vector() for song in all_songs])

        # Initialize the KNN model
        self.model = NearestNeighbors(n_neighbors=self.k, metric='cosine')
        self.model.fit(self.song_features)
    
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
        Recommends songs using the KNN algorithm.

        :param user_profile: UserProfile object representing the user's preferences.
        :return: List of recommended Song objects.
        """
        # Get the user's feature vector
        user_vector = self.get_user_vector()

        # Find the nearest neighbors
        distances, indices = self.model.kneighbors([user_vector])

        # Retrieve the recommended songs
        recommended_songs = [self.all_songs[i] for i in indices[0]]

        print('recommended songs from KNN')
        print(recommended_songs)
        
        return recommended_songs

    def __repr__(self):
        return f"KNNRecommender(all_songs_count={len(self.all_songs)}, k={self.k})"