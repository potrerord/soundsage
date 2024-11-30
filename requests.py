from Data.Song import Song
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

config_filename = "static_song_store.pkl"

CSV_FILE: str = "users.csv"
JSON_FILE: str = "user_profiles.json"

def get_recommendations(user_id):
    # Load existing song and user data
    with open(config_filename, 'rb') as config_file:
        all_songs = pickle.load(config_file)
    user_profile_store = UserProfileStore(csv_file=CSV_FILE, json_file=JSON_FILE)
    user_profile = user_profile_store.get_user_profile(user_id)

    # cold start strategy
    random_sampling_strategy: RandomSamplingStrategy = RandomSamplingStrategy(all_songs=all_songs)

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
        feedback_strategy=NewFeedbackStrategy(),
    )

    # Get the top 3 popular songs for cold start
    print("\nGetting recommended songs...")
    recommended_songs: list[Song] = recommender_aggregator.recommend()
    
    # Convert recommendations into a JSON-compatible format
    response = {
        "recommendations": [
            {
                "name": song.name,
                "artists": song.artists,
                "danceability": song.danceability,
                "energy": song.energy,
                "valence": song.valence,
                "user_id": user_id,
            }
            for song in recommended_songs
        ]
    }
    return response

def feedback_system(song_info: dict, feedback: int, user_id: str): 
    print("Got the feedback")
    print(user_id)
    print(feedback)
    print(song_info)
    

    # TODO: Use this feedback for this speicific user using FeedbackSystem. Unclear of the mechanisms as of now. 
