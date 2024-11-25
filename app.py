"""
TODO
"""

# Enable command-line functionality.
import sys
from typing import TextIO


# TODO import User

class Song:
    """Placeholder class for a song object."""

    def __init__(self):
        ...

    def __str__(self):
        ...

    ...


class Recommender:
    """Placeholder class for the recommender agent."""

    _database_filename: str
    """The name of the database file."""

    def __init__(
            self: "Recommender",
            database_filename: str,
    ) -> None:
        """Initialize a new Recommender object.
        
        Args:
            database_filename (str): The name of the database file.
        """

        self._database_filename = database_filename

    def get_song_recommendations(
            self: "Recommender",
            user_filename: str,
    ) -> list[Song]:
        """Return a list of song recommendations for a given User."""

        ...


def main() -> None:
    """Run the program."""

    # TODO Use sys.argv to specify user and database file.
    user_filename: str = sys.argv[1]
    database_filename: str = sys.argv[2]

    recommender: Recommender = Recommender(database_filename)

    recommended_song_list: list[Song] = recommender.get_song_recommendations(user_filename)

    # Write recommended songs to output file.
    outfile: TextIO
    with open(database_filename, "w") as outfile:
        song: Song
        for song in recommended_song_list:
            outfile.write(str(song) + "\n")


if __name__ == '__main__':
    main()
