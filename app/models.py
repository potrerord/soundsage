from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    user_id: str

class Song(BaseModel):
    name: str
    artists: List[str]
    danceability: float
    energy: float
    valence: float

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[Song]

# Feedback system for getting whether the song is liked or not
class FeedbackResponse(BaseModel): 
    user_id: str
    song: Song
    feedback: bool