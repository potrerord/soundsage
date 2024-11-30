from Data import Song
from RecommendationSystem import Recommender
from collections import Counter

from RecommendationSystem.ColdStart.RandomSamplingStrategy import RandomSamplingStrategy
from UserProfileSystem.UserProfile import UserProfile
from UserProfileSystem.UserProfileStore import UserProfileStore
from UserProfileSystem.FeedbackSystem.NewFeedbackStrategy import NewFeedbackStrategy


class Aggregator:
    DEFAULT_TOP_N: int = 5

    user_id: str
    user_profile_store: UserProfileStore
    user_profile: UserProfile
    recommenders: list[Recommender]
    cold_start_strategy: RandomSamplingStrategy
    feedback_strategy: NewFeedbackStrategy  # Updated to use NewFeedbackStrategy
    weights: list[float]
    top_n: int

    def __init__(
            self: "Aggregator",
            user_id: str,
            recommenders: list[Recommender],
            weights: list[float],
            user_profile_store: UserProfileStore,
            cold_start_strategy: RandomSamplingStrategy,
            feedback_strategy: NewFeedbackStrategy,  # Adding the feedback strategy
            top_n: int = DEFAULT_TOP_N,
    ) -> None:
        """Initializes the Aggregator with a list of recommenders and
        their corresponding weights.
        
        :param recommenders: List of Recommender objects to aggregate.
        :param weights: List of weights corresponding to the recommenders.
        :param feedback_strategy: Instance of feedback strategy to update user profile.
        """

        if len(recommenders) != len(weights):
            raise ValueError("The number of recommenders must be equal to the number of weights.")

        self.user_id = user_id
        self.user_profile_store = user_profile_store
        self.user_profile = user_profile_store.get_user_profile(self.user_id)
        self.recommenders = recommenders
        self.cold_start_strategy = cold_start_strategy
        self.feedback_strategy = feedback_strategy  # Initialize feedback strategy
        self.weights = weights
        self.top_n = top_n

    def recommend(self: "Aggregator") -> list[Song]:
        """
        Aggregates recommendations from multiple recommenders based on their weights and returns the top N songs.
        
        :return: List of top N recommended songs.
        """
        all_song_scores: Counter[Song] = Counter()

        if self.user_profile is None or self.user_profile.is_cold_start():
            print("\nApplying cold start strategy...")
            return self.cold_start_strategy.recommend()

        # Collect recommendations from each recommender and add scores based on weights
        recommender: Recommender
        weight: float
        for recommender, weight in zip(self.recommenders, self.weights):
            recommendations: list[Song] = recommender.recommend()

            # For each song, add the weighted score to the all_song_scores
            song: Song
            for song in recommendations:
                all_song_scores[song] += weight

        # Sort songs by total score (descending) and get the top N
        song: Song
        recommended_songs: list[Song] = [song for (song, _) in all_song_scores.most_common(self.top_n)]

        return recommended_songs

    def get_feedback(self, recommended_songs: list[Song]) -> dict[Song, int]:
        feedback: dict[Song, int] = {}
        for song in recommended_songs:
            # Simulate user feedback for each recommended song (e.g., based on user input)
            feedback[song] = int(input(f"Rate the song '{song.name} - {song.artists}' (1-5): "))
        return feedback

    def apply_feedback_to_profile(self, feedback: dict[Song, int]) -> None:
        """
        After recommendations are shown, apply feedback to the user profile.
        
        This method assumes that feedback is collected (like or dislike) from the user.
        :param feedback: The dict of recommended songs and feedback scores.
        """
        for song, score in feedback.items():
            # Update the user profile based on the feedback score
            self.feedback_strategy.update_user_profile_based_on_feedback(self.user_profile, self.user_id, song, score)
