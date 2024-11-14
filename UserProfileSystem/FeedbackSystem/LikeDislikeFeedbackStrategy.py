from UserProfileSystem import UserProfile
from Data import Song

class LikeDislikeFeedbackStrategy:
    def __init__(self, user_profile_store, like_weight: float = 1.0, dislike_weight: float = -0.5):
        """
        Initializes the LikeDislikeFeedbackStrategy with the weights for like and dislike feedback.

        :param like_weight: The weight by which to increase the feature values when a song is liked.
        :param dislike_weight: The weight by which to decrease the feature values when a song is disliked.
        """
        self.user_profile_store = user_profile_store
        self.like_weight = like_weight
        self.dislike_weight = dislike_weight

    def execute(self, user_id: str, song: Song, liked: bool):
        """
        Executes the feedback strategy and updates the user profile based on whether the song was liked or disliked.

        :param userProfile: The UserProfile instance to be updated.
        :param song: The Song instance that received feedback.
        :param liked: Boolean indicating whether the song was liked (True) or disliked (False).
        """
        user_profile = self.user_profile_store.get_user_profile(user_id)
        
        # Define the weight based on feedback
        feedback_weight = self.like_weight if liked else self.dislike_weight

        # Update numerical features in the user profile based on feedback
        user_profile.danceability += feedback_weight * song.danceability
        user_profile.energy += feedback_weight * song.energy
        user_profile.valence += feedback_weight * song.valence
        user_profile.acousticness += feedback_weight * song.acousticness
        user_profile.tempo += feedback_weight * song.tempo
        user_profile.loudness += feedback_weight * song.loudness

        # Update genres and artists based on the feedback (liked or disliked)
        # If liked, increase weight for the genre and artist; if disliked, decrease it
        if liked:
            # user_profile.genres.update(song.genres)
            user_profile.artists.update(song.artists)
        else:
            # user_profile.genres.subtract(song.genres)
            user_profile.artists.subtract(song.artists)

        # Optionally track which songs are liked/disliked for further analysis (popularity, etc.)
        if liked:
            user_profile.popular_tracks.update([song.track_id])
        else:
            user_profile.popular_tracks.subtract([song.track_id])

        # Update song count (not strictly necessary, but could help track the number of interactions)
        user_profile.song_count += 1

        self.user_profile_store.update_user_profile(user_id, user_profile)

        # Normalize/adjust features if needed based on the number of feedbacks
        # Example: You might choose to divide by song_count to keep features from growing unbounded over time