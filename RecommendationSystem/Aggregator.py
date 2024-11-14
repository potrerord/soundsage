from Data import Song
from RecommendationSystem import Recommender
from collections import Counter
import numpy as np

class Aggregator:
    def __init__(self, user_id: str, recommenders: [Recommender], weights: [float], user_profile_store, cold_start_strategy):
        """
        Initializes the Aggregator with a list of recommenders and their corresponding weights.
        
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

    def recommend(self, top_n: int = 5) -> [Song]:
        """
        Aggregates recommendations from multiple recommenders based on their weights and returns the top N songs.
        
        :param top_n: Number of songs to return as recommendations.
        :return: List of top N recommended songs.
        """
        all_song_scores = Counter()

        user_profile = self.user_profile_store.get_user_profile(self.user_id)

        if not user_profile or user_profile.is_cold_start():
            return self.cold_start_strategy.recommend()

        # Collect recommendations from each recommender and add scores based on weights
        for recommender, weight in zip(self.recommenders, self.weights):
            recommendations = recommender.recommend(top_n)
            
            # For each song, add the weighted score to the all_song_scores
            for song in recommendations:
                all_song_scores[song] += weight
        
        # Sort songs by total score (descending) and get the top N
        recommended_songs = [song for song, _ in all_song_scores.most_common(top_n)]
        
        return recommended_songs