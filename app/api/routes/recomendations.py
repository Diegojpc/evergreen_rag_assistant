from fastapi import APIRouter, Body, HTTPException, Depends

from app.models.recommendations import RecommendationRequest, RecommendationResponse
from app.domain.recommendations import RecommendationDomain

recomendations_router: APIRouter = APIRouter(
    prefix="/recomendations",
    tags=["Process Recommendations"],
)

@recomendations_router.post(
    path="/",
    description="Get recommendations for a process based on a parcel id and a user query",
    response_model=RecommendationResponse,
)

def get_recommendation_domain() -> RecommendationDomain:
    """Dependency function to create/get RecommendationDomain instance."""
    return RecommendationDomain()

def get_recomendations(
    request: RecommendationRequest = Body(
        ...,
        description="The request object containing the parcel id and user query",
    ),
    recommendation_domain: RecommendationDomain = Depends(get_recommendation_domain)
) -> RecommendationResponse:
    """
    Generate process recommendations based on a parcel ID and user query.

    This endpoint processes a request containing a parcel ID and user query to generate
    relevant process recommendations. It uses the recommendation domain to process the
    request and return appropriate recommendations.

    Args:
        request (RecommendationRequest): The request object containing:
            - parcel_id: The unique identifier of the parcel
            - query: The user's query for which recommendations are needed

    Returns:
        RecommendationResponse: A response object containing:
            - recommendations: List of recommended processes
            - confidence_scores: Associated confidence scores for each recommendation
            - metadata: Additional information about the recommendations
    """

    try:
        return recommendation_domain.get_recommendations(request)

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")