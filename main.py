import sys

from ctypes import DEFAULT_MODE
import os
from Data.Song import Song
from Data.SongStore import SongStore
from RecommendationSystem.Aggregator import Aggregator
from RecommendationSystem.Algorithms.CosineSimiliarity import CosineSimilarity
from RecommendationSystem.Algorithms.KNN import KNNRecommender
from RecommendationSystem.ColdStart.RandomSamplingStrategy import RandomSamplingStrategy
from UserProfileSystem.FeedbackSystem.NewFeedbackStrategy import NewFeedbackStrategy
from UserProfileSystem.UserProfile import UserProfile
from UserProfileSystem.UserProfileStore import UserProfileStore
from RecommendationSystem.Recommender import FeaturePrioritizationRecommender

SONG_DATABASE_CSV: str = "tracks_features.csv"
USERS_DATABASE_CSV: str = "users.csv"
# USERS_DATABASE_CSV = "mock_users.csv"
USER_PLAYLIST_CSV: str = "Data/adn-spotify-playlist_features-runaway.csv"
USERS_DATABASE_JSON = 'user_profiles.json'

DEFAULT_USER_ID: str = "1"


def main() -> None:
    print("Current Working Directory:", os.getcwd())

    print(f"\nWelcome to SoundSage!")

    # Load the dataset into memory.
    print(f"\nLoading song data into memory from '{SONG_DATABASE_CSV}'...")

    song_store: SongStore = SongStore(file_name=SONG_DATABASE_CSV)

    # Get list of all songs from data.
    print("\nGetting all songs...")
    all_songs: list[Song] = song_store.get_all_songs()

    # Read user profile.
    print("\nReading user profile...")
    user_profile_store: UserProfileStore = UserProfileStore(USER_PLAYLIST_CSV, USERS_DATABASE_JSON)
    print("\nGetting user profile")
    print(user_profile_store)

    user_profile: UserProfile = user_profile_store.get_user_profile(DEFAULT_USER_ID)
    user_profile_store: UserProfileStore = UserProfileStore(USER_PLAYLIST_CSV, USERS_DATABASE_JSON)
    user_profile: UserProfile = UserProfile.create_profile_from_songs_csv(DEFAULT_USER_ID, USER_PLAYLIST_CSV)

    # Validate user profile features.
    user_profile.validate_features()
    print(f"\nUser profile:\n{user_profile}")

    if user_profile is None:
        print(f"\nCreating new user...")
        user_profile_store.update_user_profile(user_id=DEFAULT_USER_ID,
                                               user_profile=UserProfile(user_id=DEFAULT_USER_ID))

    # cold start strategy
    random_sampling_strategy: RandomSamplingStrategy = RandomSamplingStrategy(all_songs=all_songs)

    # feedback strategy
    feedback_strategy: NewFeedbackStrategy = NewFeedbackStrategy()

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
        feedback_strategy=feedback_strategy,  # Pass feedback strategy to aggregator
    )

    # Get the top 3 popular songs for cold start
    print("\nGetting recommended songs...")
    recommended_songs: list[Song] = recommender_aggregator.recommend()

    print(f"\nRecommended songs: [")
    i: int = 0
    for song in recommended_songs:
        print(f"    ({i}) {song}")
        print(f"           Acousticness:     {song.acousticness:10.4f}")
        print(f"           Danceability:     {song.danceability:10.4f}")
        print(f"           Energy:           {song.energy:10.4f}")
        print(f"           Instrumentalness: {song.instrumentalness:10.4f}")
        print(f"           Liveness:         {song.liveness:10.4f}")
        print(f"           Loudness:         {song.loudness:10.4f}")
        print(
            f"           Popularity:       {song.popularity:10.4f}" if song.popularity is not None else f"           Popularity:             None")
        print(f"           Speechiness:      {song.speechiness:10.4f}")
        print(f"           Tempo:            {song.tempo:10.4f}")
        print(f"           Valence:          {song.valence:10.4f}")
        i += 1
    print("]")

    # Collect feedback from the user for each recommended song
    print("\nProviding feedback...")
    for song in recommended_songs:
        # Prompt the user for feedback on the recommended song
        feedback_score = int(input(f"Rate the song '{song.name}' (1-5): "))

        # Update user profile based on feedback using NewFeedbackStrategy
        feedback_strategy.update_user_profile_based_on_feedback(user_profile, DEFAULT_USER_ID, song, feedback_score)

    # Print the updated user profile after feedback
    print("\nUpdated user profile after feedback:")
    user_profile = user_profile_store.get_user_profile(DEFAULT_USER_ID)
    print(user_profile)


if __name__ == "__main__":
    main()
