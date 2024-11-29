from fastapi import APIRouter
from app.services import get_recommendations
from app.models import RecommendationRequest, RecommendationResponse, FeedbackResponse

router = APIRouter()

@router.post("/recommendations", response_model=RecommendationResponse)
def recommendations(request: RecommendationRequest):
    """
    Generate music recommendations based on user ID.
    """
    return get_recommendations(request.user_id)

@router.post("/feedback", response_model=FeedbackResponse)
def feedback(request: RecommendationRequest):
    """
    Generate music recommendations based on user ID.
    """
    return get_recommendations(request.user_id)
