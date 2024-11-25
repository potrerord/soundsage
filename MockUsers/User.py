
class User:
    def __init__(self, user_id, liked_tracks):
        """
        Initialize a mock user with a user ID and liked tracks.

        :param user_id: Unique identifier for the user
        :param liked_tracks: List of track IDs that the user likes
        """
        self.user_id = user_id
        self.liked_tracks = liked_tracks  # User's liked tracks (list of track IDs)

    def __repr__(self):
        return f"User(user_id={self.user_id}, liked_tracks={self.liked_tracks})"
