import json
from Data.Song import Song
from Data.SongStore import SongStore
from RecommendationSystem.Aggregator import Aggregator
from RecommendationSystem.Algorithms.CosineSimiliarity import CosineSimilarity
from RecommendationSystem.Algorithms.KNN import KNNRecommender
from RecommendationSystem.ColdStart.RandomSamplingStrategy import RandomSamplingStrategy
from UserProfileSystem.FeedbackSystem.LikeDislikeFeedbackStrategy import LikeDislikeFeedbackStrategy
from UserProfileSystem.UserProfile import UserProfile
from UserProfileSystem.UserProfileStore import UserProfileStore
from RecommendationSystem.Recommender import FeaturePrioritizationRecommender
import pickle

song_store = SongStore("tracks_features.csv")
# Data to be written
config_data = song_store.get_all_songs()
config_filename = "static_song_store.pkl"

# Writing the dictionary to a file in JSON format
with open(config_filename, 'wb') as config_file:
    pickle.dump(config_data, config_file)

print(f"Data successfully written to {config_filename}")