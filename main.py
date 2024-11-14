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

    user_id = "1"
    user_profile_store = UserProfileStore(file_name="users.csv")
    print("reading user profile")
    user_profile = user_profile_store.get_user_profile(user_id=user_id)
    print(user_profile)

    if user_profile is None: 
        print("new user")
        user_profile_store.update_user_profile(user_id=user_id, user_profile=UserProfile(user_id=user_id))

    # cold start strategy
    random_sampling_strategy = RandomSamplingStrategy(all_songs=all_songs)

    # feedback strategy
    like_dislike_feedback_strategy = LikeDislikeFeedbackStrategy(user_profile_store=user_profile_store)

    # recommendation algorithms
    cosine_similarity = CosineSimilarity(user_profile=user_profile, all_songs=all_songs)

    # recommender
    recommender = Aggregator(user_id="1", recommenders=[cosine_similarity], weights=[1.0], user_profile_store=user_profile_store, cold_start_strategy=random_sampling_strategy, feedback_strategy=like_dislike_feedback_strategy)
    
    # Get the top 3 popular songs for cold start
    recommended_songs = recommender.recommend()

    print("recommended songs")
    print(recommended_songs)

    print("providing mock feedback")
    like_dislike_feedback_strategy.execute(user_id=user_id, song=recommended_songs[0], liked=True)
    like_dislike_feedback_strategy.execute(user_id=user_id, song=recommended_songs[1], liked=False)
    
    print("updated user profile after feedback")
    print(user_profile)
