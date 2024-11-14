from Data.SongStore import SongStore
from RecommendationSystem.Aggregator import Aggregator
from RecommendationSystem.Algorithms.CosineSimiliarity import CosineSimilarity
from UserProfileSystem.UserProfile import UserProfile

if __name__ == "__main__":
    # Example list of Song objects with popularity attribute
    song_store = SongStore(file_name='tracks_features.csv')
    all_songs = song_store.get_all_songs()
    
    print("printing all songs length: ", len(all_songs))
    user_profile = UserProfile(user_id="1")

    cosine_similarity = CosineSimilarity(user_profile=user_profile, all_songs=all_songs)
    recommender = Aggregator(recommenders=[cosine_similarity], weights=[1.0])
    
    # Get the top 3 popular songs for cold start
    recommended_songs = recommender.recommend()
    
    # Print recommended songs
    for song in recommended_songs:
        print(f"Recommended Song: {song.track_id} - {song.artist} (Popularity: {song.popularity})")