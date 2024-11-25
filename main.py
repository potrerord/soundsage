from Data.Song import Song
from Data.SongStore import SongStore
from RecommendationSystem.Aggregator import Aggregator
from RecommendationSystem.Algorithms.CosineSimiliarity import CosineSimilarity
from RecommendationSystem.Algorithms.KNN import KNNRecommender
from RecommendationSystem.ColdStart.RandomSamplingStrategy import RandomSamplingStrategy
from UserProfileSystem.FeedbackSystem.LikeDislikeFeedbackStrategy import LikeDislikeFeedbackStrategy
from UserProfileSystem.UserProfile import UserProfile
from UserProfileSystem.UserProfileStore import UserProfileStore

DATA_FILENAME: str = "tracks_features.csv"
USER_FILENAME: str = "users.csv"

DEFAULT_USER_ID: str = "1"


def main() -> None:
    print(f"\nWelcome to SoundSage!")
    # Load the dataset into memory.
    print(f"\nLoading song data into memory from '{DATA_FILENAME}'...")
    song_store: SongStore = SongStore(file_name=DATA_FILENAME)

    # Get list of all songs from data.
    print("\nGetting all songs...")
    all_songs: list[Song] = song_store.get_all_songs()

    # Read user profile.
    print("\nReading user profile...")
    user_profile_store: UserProfileStore = UserProfileStore(file_name=USER_FILENAME)
    user_profile: UserProfile = user_profile_store.get_user_profile(user_id=DEFAULT_USER_ID)
    print(f"\nUser profile:\n{user_profile}")

    if user_profile is None:
        print(f"\nCreating new user...")
        user_profile_store.update_user_profile(user_id=DEFAULT_USER_ID,
                                               user_profile=UserProfile(user_id=DEFAULT_USER_ID))

    # cold start strategy
    random_sampling_strategy: RandomSamplingStrategy = RandomSamplingStrategy(all_songs=all_songs)

    # feedback strategy
    like_dislike_feedback_strategy: LikeDislikeFeedbackStrategy = LikeDislikeFeedbackStrategy(
        user_profile_store=user_profile_store)

    # recommendation algorithms
    cosine_similarity: CosineSimilarity = CosineSimilarity(user_profile=user_profile, all_songs=all_songs)
    knn: KNNRecommender = KNNRecommender(user_profile=user_profile, all_songs=all_songs)

    # recommender
    recommender_aggregator: Aggregator = Aggregator(
        user_id="1",
        recommenders=[cosine_similarity, knn],
        weights=[0.2, 0.8],
        user_profile_store=user_profile_store,
        cold_start_strategy=random_sampling_strategy,
    )

    # Get the top 3 popular songs for cold start
    print("\nGetting recommended songs...")
    recommended_songs: list[Song] = recommender_aggregator.recommend()

    print(f"\nRecommended songs:\n{"\n".join([str(song) for song in recommended_songs])}")

    print("\nProviding mock feedback...")
    like_dislike_feedback_strategy.execute(user_id=DEFAULT_USER_ID, song=recommended_songs[0], liked=True)
    like_dislike_feedback_strategy.execute(user_id=DEFAULT_USER_ID, song=recommended_songs[1], liked=False)

    print("\nUpdated user profile after feedback:")
    print(user_profile)


if __name__ == "__main__":
    main()
