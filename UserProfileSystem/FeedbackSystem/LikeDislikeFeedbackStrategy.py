from UserProfileSystem import UserProfile
from Data import Song

class LikeDislikeFeedbackStrategy:
    def __init__(self, like_weight: float = 1.0, dislike_weight: float = -0.5):
        """
        Initializes the LikeDislikeFeedbackStrategy with the weights for like and dislike feedback.

        :param like_weight: The weight by which to increase the feature values when a song is liked.
        :param dislike_weight: The weight by which to decrease the feature values when a song is disliked.
        """
        self.like_weight = like_weight
        self.dislike_weight = dislike_weight

    def execute(self, userProfile: UserProfile, song: Song, liked: bool):
        """
        Executes the feedback strategy and updates the user profile based on whether the song was liked or disliked.

        :param userProfile: The UserProfile instance to be updated.
        :param song: The Song instance that received feedback.
        :param liked: Boolean indicating whether the song was liked (True) or disliked (False).
        """
        # Define the weight based on feedback
        feedback_weight = self.like_weight if liked else self.dislike_weight

        # Update numerical features in the user profile based on feedback
        userProfile.danceability += feedback_weight * song.danceability
        userProfile.energy += feedback_weight * song.energy
        userProfile.valence += feedback_weight * song.valence
        userProfile.acousticness += feedback_weight * song.acousticness
        userProfile.tempo += feedback_weight * song.tempo
        userProfile.loudness += feedback_weight * song.loudness

        # Update genres and artists based on the feedback (liked or disliked)
        # If liked, increase weight for the genre and artist; if disliked, decrease it
        if liked:
            userProfile.genres.update(song.genres)
            userProfile.artists.update([song.artist])
        else:
            userProfile.genres.subtract(song.genres)
            userProfile.artists.subtract([song.artist])

        # Optionally track which songs are liked/disliked for further analysis (popularity, etc.)
        if liked:
            userProfile.popular_tracks.update([song.track_id])
        else:
            userProfile.popular_tracks.subtract([song.track_id])

        # Update song count (not strictly necessary, but could help track the number of interactions)
        userProfile.song_count += 1

        # Normalize/adjust features if needed based on the number of feedbacks
        # Example: You might choose to divide by song_count to keep features from growing unbounded over time