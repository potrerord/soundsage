from Data.Song import Song
import Data.constants as c
from Data.SongStore import SongStore
from RecommendationSystem.Aggregator import Aggregator
from RecommendationSystem.Algorithms.CosineSimiliarity import CosineSimilarity
from RecommendationSystem.Algorithms.KNN import KNNRecommender
from RecommendationSystem.ColdStart.RandomSamplingStrategy import RandomSamplingStrategy
from UserProfileSystem.FeedbackSystem.FeedbackStrategy import FeedbackStrategy
from UserProfileSystem.FeedbackSystem.LikeDislikeFeedbackStrategy import LikeDislikeFeedbackStrategy
from UserProfileSystem.FeedbackSystem.NewFeedbackStrategy import NewFeedbackStrategy
from UserProfileSystem.UserProfile import UserProfile
from UserProfileSystem.UserProfileStore import UserProfileStore
from RecommendationSystem.Recommender import FeaturePrioritizationRecommender
import pickle
import os

config_filename = "static_song_store.pkl"
recommender_file = "static_recommender.pkl"
userstore_file = "static_userstore.pkl"

SONG_DATABASE_CSV: str = "tracks_features.csv"
USERS_DATABASE_CSV: str = "users.csv"
# USERS_DATABASE_CSV = "mock_users.csv"
USER_PLAYLIST_CSV: str = "Data/adn-spotify-playlist_features-runaway.csv"
USERS_DATABASE_JSON = 'user_profiles.json'

COSINE_SIMILARITY_WEIGHT: float = 0.5
KNN_WEIGHT: float = 0.5

def get_recommendations(user_id: str):
    print("Current Working Directory:", os.getcwd())

    print(f"\nWelcome to SoundSage!")

    # Load existing song and user data
    print(f"\nLoading song data from {os.path.realpath(config_filename)}")
    with open(config_filename, 'rb') as config_file:
        all_songs = pickle.load(config_file)
    # Load user profile database from file.
    # TODO: are we using csv or json user database?
    print(
        f"\nLoading user profile database from '{os.path.realpath(USERS_DATABASE_CSV)}' or '{os.path.realpath(USERS_DATABASE_JSON)}'...")
    user_profile_store: UserProfileStore = UserProfileStore(USERS_DATABASE_CSV, USERS_DATABASE_JSON)

    # Get user profile.
    print(f"\nLoading user profile ID#{user_id}...")
    user_profile: UserProfile = user_profile_store.get_user_profile(user_id)
    if user_profile is None:
        print(
            f"\nUser profile ID#{user_id} not found. Creating user profile ID#{user_id} from songs CSV '{os.path.realpath(USER_PLAYLIST_CSV)}'...")
        user_profile: UserProfile = UserProfile.create_profile_from_songs_csv(user_id, USER_PLAYLIST_CSV)

    # Validate user profile.
    user_profile.validate_features()
    print(f"\nUser profile ID#{user_profile.user_id}:\n{user_profile}")

    # cold start strategy
    random_sampling_strategy: RandomSamplingStrategy = RandomSamplingStrategy(all_songs=all_songs)

    # feedback strategy
    feedback_strategy: NewFeedbackStrategy = NewFeedbackStrategy()

    # recommendation algorithms
    cosine_similarity: CosineSimilarity = CosineSimilarity(user_profile=user_profile, all_songs=all_songs)
    knn: KNNRecommender = KNNRecommender(user_profile=user_profile, all_songs=all_songs)

    # recommender
    recommender_aggregator: Aggregator = Aggregator(
        user_id=user_id,
        recommenders=[cosine_similarity, knn],
        weights=[COSINE_SIMILARITY_WEIGHT, KNN_WEIGHT],
        user_profile_store=user_profile_store,
        cold_start_strategy=random_sampling_strategy,
        feedback_strategy=feedback_strategy,  # Pass feedback strategy to aggregator
    )
    create_static_data(recommender_file, "wb", recommender_aggregator)
    create_static_data(userstore_file, "wb", user_profile_store)
    # Get the top 3 popular songs for cold start
    print("\nGetting recommended songs...")
    recommended_songs: list[Song] = recommender_aggregator.recommend()

    # Convert recommendations into a JSON-compatible format
    # response = {
    #     "recommendations": [
    #         {
    #             "name": song.name,
    #             "artists": song.artists,
    #             "danceability": song.danceability,
    #             "energy": song.energy,
    #             "valence": song.valence,
    #             "user_id": user_id,
    #         }
    #         for song in recommended_songs
    #     ]
    # }
    response = {
        "recommendations": [
            {
                "name": song.name,
                "artists": song.artists,
                "acousticness": song.acousticness,
                "danceability": song.danceability,
                "energy": song.energy,
                "instrumentalness": song.instrumentalness,
                "liveness": song.liveness,
                "loudness": song.loudness,
                "speechiness": song.speechiness,
                "tempo": song.tempo,
                "valence": song.valence,
                "user_id": user_id,
            }
            for song in recommended_songs
        ]
    }   
    return response


def feedback_system(song_info: dict, rating: int, user_id: str):
    print("Got the feedback")
    print(user_id)
    print(rating)
    print(song_info)

    # recommender
    recommender_aggregator: Aggregator = load_static_data(recommender_file, "rb")
    user_profile_store = load_static_data(userstore_file, "rb")
    # Collect feedback from the user for each recommended song
    print("\nProviding feedback...")
    # Build the song object
    feedback_song = Song(id=None, album=None, album_id=None, artist_ids=None, track_number=0, disc_number=0, explicit=False, key=c.KEY_MIN, mode=c.MODE_MINOR, duration_ms=0, time_signature=c.TIME_SIG_MIN, year=2000, release_date=2000, popularity=None, name=song_info["name"], artists=song_info["artists"], acousticness=song_info["acousticness"], 
                            danceability=song_info["danceability"], energy=song_info["energy"], instrumentalness=song_info["instrumentalness"], 
                            liveness=song_info["liveness"], loudness=song_info["loudness"], speechiness=song_info["speechiness"], tempo=song_info["tempo"], valence=song_info["valence"], 
                            )
    feedback = {feedback_song: rating}
    recommender_aggregator.apply_feedback_to_profile(feedback)

    # Print the updated user profile after feedback
    print("\nUpdated user profile after feedback:")
    user_profile = user_profile_store.get_user_profile(user_id)
    print(user_profile)

    # TODO: Use this feedback for this speicific user using FeedbackSystem. Unclear of the mechanisms as of now.

def create_static_data(file_name, mode, data): 
    # Writing the dictionary to a file in JSON format
    with open(file_name, mode) as config_file:
        pickle.dump(data, config_file)

    print(f"Data successfully written to {file_name}")

def load_static_data(input_file, mode): 
    print("Loading from static data")
    with open(input_file, mode) as config_file:
        data = pickle.load(config_file)
        print(f"Finish loading from static data from {input_file}")
        return data
    return None