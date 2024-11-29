from fastapi import APIRouter
from app.services import get_recommendations
from app.models import RecommendationRequest, RecommendationResponse

router = APIRouter()

@router.post("/recommendations", response_model=RecommendationResponse)
def recommendations(request: RecommendationRequest):
    """
    Generate music recommendations based on user ID.
    """
    return get_recommendations(request.user_id)
