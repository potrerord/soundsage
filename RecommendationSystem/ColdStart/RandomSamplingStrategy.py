from RecommendationSystem import Recommender
from RecommendationSystem.ColdStart import ColdStart
from Data import Song

class RandomSamplingStrategy(ColdStart):
    def __init__(self, all_songs: [Song], top_n: int = 5):
        """
        Initializes the RandomSamplingStrategy with a list of all songs and the number of recommendations.

        :param all_songs: List of all available Song objects.
        :param top_n: Number of top popular songs to return.
        """
        self.all_songs = all_songs
        self.top_n = top_n

    def recommend(self) -> [Song]:
        """
        Recommends the top N most popular songs by frequency from the dataset for cold start.

        :return: List of top N most popular Song objects.
        """
        # Sort the songs by popularity (assuming popularity is represented by play count or similar metric)
        # For simplicity, let's assume that the "popularity" is an attribute of the song class
        sorted_songs = sorted(self.all_songs, key=lambda song: song.popularity, reverse=True)
        
        # Return the top N songs
        return sorted_songs[:self.top_n]