from Data.SongStore import SongStore
from RecommendationSystem.Aggregator import Aggregator
from RecommendationSystem.Algorithms.CosineSimiliarity import CosineSimilarity
from RecommendationSystem.ColdStart.RandomSamplingStrategy import RandomSamplingStrategy
from UserProfileSystem.FeedbackSystem.LikeDislikeFeedbackStrategy import LikeDislikeFeedbackStrategy
from UserProfileSystem.UserProfile import UserProfile
from UserProfileSystem.UserProfileStore import UserProfileStore

if __name__ == "__main__":
    song_store = SongStore(file_name='tracks_features.csv')
    all_songs = song_store.get_all_songs()

    print("printing all songs length: ", len(all_songs))
    user_profile_store = UserProfileStore(file_name="users.csv")
    user_profile = user_profile_store.get_user_profile("1")

    cold_start_strategy = RandomSamplingStrategy(all_songs=all_songs)
    cosine_similarity = CosineSimilarity(user_profile=user_profile, all_songs=all_songs)
    recommender = Aggregator(user_id="1", recommenders=[cosine_similarity], weights=[1.0], user_profile_store=user_profile_store, cold_start_strategy=cold_start_strategy)
    
    # Get the top 3 popular songs for cold start
    recommended_songs = recommender.recommend()

    like_dislike_feedback_strategy = LikeDislikeFeedbackStrategy()

    print(recommended_songs)