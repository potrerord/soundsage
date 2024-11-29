from RecommendationSystem.Aggregator import Aggregator
from Data.SongStore import SongStore
from UserProfileSystem.UserProfileStore import UserProfileStore

def get_recommendations(user_id: str):
    # Load existing song and user data
    song_store = SongStore("Data/tracks_features.csv")
    user_profile_store = UserProfileStore("Data/users.csv")
    user_profile = user_profile_store.get_user_profile(user_id)

    # Create and aggregate recommendations
    all_songs = song_store.get_all_songs()
    aggregator = Aggregator(
        user_id=user_id,
        recommenders=[],  # Add your existing recommenders
        weights=[],
        user_profile_store=user_profile_store
    )
    recommendations = aggregator.recommend()
    
    # Convert recommendations into a JSON-compatible format
    response = {
        "user_id": user_id,
        "recommendations": [
            {
                "name": song.name,
                "artists": song.artists,
                "danceability": song.danceability,
                "energy": song.energy,
                "valence": song.valence
            }
            for song in recommendations
        ]
    }
    return response
