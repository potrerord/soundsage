from abc import ABC, abstractmethod

from Data import Song


class Recommender:
    @abstractmethod
    def recommend(self) -> list[Song]:
        ...
