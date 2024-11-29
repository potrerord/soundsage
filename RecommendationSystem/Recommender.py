from abc import ABC, abstractmethod
from Data import Song, SongStore
import numpy as np
import pandas as pd


class Recommender(ABC):
    @abstractmethod
    def recommend(self) -> list[Song]:
        ...


class FeaturePrioritizationRecommender(Recommender):
    def __init__(self, user_data, song_store: SongStore):
        """
        :param user_data: DataFrame containing user's listening history.
        :param song_store: Instance of SongStore to access song features.
        """
        self.user_data = user_data
        self.song_store = song_store

    def prioritize_features(self):
        """
        Calculate the importance of each feature for a user based on standard deviation.
        :return: A dictionary with feature names and their calculated weights.
        """
        # Collect song features from the user's listening history
        songs = self.user_data["song_id"].map(self.song_store.get_song_by_id)
        feature_df = pd.DataFrame([song.to_dict() for song in songs])

        # Calculate standard deviation of features
        feature_std = feature_df.std()

        # Normalize weights (optional)
        weights = feature_std / feature_std.sum()

        return weights.to_dict()

    def recommend(self) -> list[Song]:
        """
        Generate recommendations by prioritizing features based on user data.
        :return: A list of recommended songs.
        """
        # Prioritize features
        feature_weights = self.prioritize_features()

        # Retrieve all songs from the store
        all_songs = self.song_store.get_all_songs()

        # Calculate weighted scores for each song
        recommendations = []
        for song in all_songs:
            score = sum(
                song.features[feature] * weight
                for feature, weight in feature_weights.items()
                if feature in song.features
            )
            recommendations.append((song, score))

        # Sort by score in descending order
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

        # Return the top recommendations
        return [rec[0] for rec in recommendations[:10]]  # Top 10 recommendations
