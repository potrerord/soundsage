import random
from Data import Song

class RandomSamplingStrategy:
    def __init__(self, all_songs: [Song], top_n: int = 5):
        """
        Initializes the RandomSamplingStrategy with a list of all songs and the number of recommendations.

        :param all_songs: List of all available Song objects.
        :param top_n: Number of random songs to return.
        """
        self.all_songs = all_songs
        self.top_n = top_n

    def recommend(self) -> [Song]:
        """
        Recommends the top N random songs from the dataset for cold start.

        :return: List of N randomly selected Song objects.
        """
        # Randomly select top N songs from the list of all songs
        random_songs = random.sample(self.all_songs, self.top_n)
        
        # Return the list of randomly selected songs
        return random_songs