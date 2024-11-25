from Data import Song
from RecommendationSystem import Recommender
from collections import Counter
import numpy as np

from RecommendationSystem.ColdStart.RandomSamplingStrategy import RandomSamplingStrategy
from UserProfileSystem.UserProfile import UserProfile
from UserProfileSystem.UserProfileStore import UserProfileStore


class Aggregator:
    DEFAULT_TOP_N: int = 5

    def __init__(
            self: "Aggregator",
            user_id: str,
            recommenders: list[Recommender],
            weights: list[float],
            user_profile_store: UserProfileStore,
            cold_start_strategy: RandomSamplingStrategy,
            top_n: int = DEFAULT_TOP_N,
    ) -> None:
        """Initializes the Aggregator with a list of recommenders and
        their corresponding weights.
        
        :param recommenders: List of Recommender objects to aggregate.
        :param weights: List of weights corresponding to the recommenders.
        """

        if len(recommenders) != len(weights):
            raise ValueError("The number of recommenders must be equal to the number of weights.")

        self.user_id = user_id
        self.user_profile_store = user_profile_store
        self.recommenders = recommenders
        self.cold_start_strategy = cold_start_strategy
        self.weights = weights
        self.top_n = top_n

    def recommend(self: "Aggregator") -> list[Song]:
        """
        Aggregates recommendations from multiple recommenders based on their weights and returns the top N songs.
        
        :param top_n: Number of songs to return as recommendations.
        :return: List of top N recommended songs.
        """
        all_song_scores: Counter = Counter()

        user_profile: UserProfile = self.user_profile_store.get_user_profile(self.user_id)

        if user_profile is None or user_profile.is_cold_start():
            print('applying cold start strategy')
            return self.cold_start_strategy.recommend()

        # Collect recommendations from each recommender and add scores based on weights
        recommender: Recommender
        weight: float
        for recommender, weight in zip(self.recommenders, self.weights):
            recommendations = recommender.recommend()

            # For each song, add the weighted score to the all_song_scores
            song: Song
            for song in recommendations:
                all_song_scores[song] += weight

        # Sort songs by total score (descending) and get the top N
        recommended_songs: list[Song] = [song for song, _ in all_song_scores.most_common(self.top_n)]

        return recommended_songs
