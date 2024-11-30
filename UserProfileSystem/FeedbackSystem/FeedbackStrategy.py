from abc import ABC, abstractmethod

from UserProfileSystem import UserProfile

class FeedbackStrategy(ABC):
    @abstractmethod
    def execute(self, userProfile: UserProfile):
        pass