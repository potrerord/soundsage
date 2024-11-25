from abc import ABC, abstractmethod

from Data import Song

class Recommender(ABC):
    @abstractmethod
    def recommend(self) -> [Song]:
        pass