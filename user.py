"""
@brief A synthetic User to provide feedback to SoundSage algorithm.
"""


class User:
    """A synthetic 'user' with musical preferences that can provide
     feedback to the SoundSage algorithm on the fitness of
     recommendations.
     """

    _id: int
    """The user ID number."""

    _liked_songs: list[str]
    """The song list that represents the user's liked songs."""

    _liked_genres: list[str]
    """List of genres that this user likes."""

    # TODO: Add more preferences (acousticness(?), etc.)

    def __init__(
            self: "User",
    ) -> None:
        """Instantiate a new User object."""

        # TODO: Add constructor parameters.
        ...

    def rate_song_list(
            self: "User",
            song_list: list[str],
    ) -> float:
        """Get the user's rating of a song list.
        
        :param song_list: the song list to rate
        
        :return: the rating of the song list.
        """

        # TODO: Process song list according to user preferences.

        # TODO: Condense into a float in range [0, 1] ?
        ...

    def get_id(self: "User") -> int:
        """Get the user ID number.
        
        :return: the user ID number.
        """

        return self._id

    def get_liked_songs(self: "User") -> list[str]:
        """Get the user's liked songs.
        
        :return: the user's liked songs.
        '"""

        return self._liked_songs

    def get_liked_genres(self: "User") -> list[str]:
        """Get the user's liked genres.
        
        :return: the user's liked genres.
        """

        return self._liked_genres

    def set_id(self: "User", id: int) -> None:
        """Set the user ID number.
        
        :param id: the user ID number
        """

        self._id = id

    def set_liked_songs(
            self: "User",
            liked_songs: list[str],
    ) -> None:
        """Set the user's song history.
        
        :param liked_songs: the user's song history
        """

        self._liked_songs = liked_songs

    def set_liked_genres(
            self: "User",
            liked_genres: list[str]
    ) -> None:
        """Set the user's liked genres.
        
        :param liked_genres: the user's liked genres
        """

        self._liked_genres = liked_genres
