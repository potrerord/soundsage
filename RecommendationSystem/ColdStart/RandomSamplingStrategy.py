import random
from Data import Song
from RecommendationSystem.Recommender import Recommender


class RandomSamplingStrategy(Recommender):
    DEFAULT_TOP_N: int = 5

    def __init__(
            self: "RandomSamplingStrategy",
            all_songs: list[Song],
            top_n: int = DEFAULT_TOP_N,
    ) -> None:
        """
        Initializes the RandomSamplingStrategy with a list of all songs and the number of recommendations.

        :param all_songs: List of all available Song objects.
        :param top_n: Number of random songs to return.
        """
        self.all_songs = all_songs
        self.top_n = top_n

    def recommend(self: "RandomSamplingStrategy") -> list[Song]:
        """
        Recommends the top N random songs from the dataset for cold start.

        :return: List of N randomly selected Song objects.
        """
        # Randomly select top N songs from the list of all songs
        random_songs: list[Song] = random.sample(self.all_songs, self.top_n)

        # Return the list of randomly selected songs
        return random_songs
