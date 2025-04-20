from pydantic import BaseModel

from app.models.llms import ImplementedModels


class RecommendationRequest(BaseModel):
    """
    A request model for getting agricultural recommendations based on project and user query.

    This model is used to structure the input data needed to generate recommendations
    for agricultural actions and decisions.

    Attributes:
        model (ImplementedModels): The model to use for the recommendation.
        parcel_id (str): The unique identifier of the parcel
        user_question (str): The user's question or query about agricultural actions.
                             Defaults to a standard query about next 5-7 day actions.
    """

    model: ImplementedModels = ImplementedModels.GPT_OPENAI_4O
    parcel_id: str
    user_question: str = "What actions should I take on my crop over the next 5-7 days?"


class RecommendationResponse(BaseModel):
    """
    A response model containing agricultural recommendations for a specific parcel.

    This model structures the output data containing recommendations generated
    based on the user's query and parcel information.

    Attributes:
        model (ImplementedModels): The model used to generate the recommendations
        project_id (str): The unique identifier of the project associated with the parcel
        parcel_id (str): The unique identifier of the parcel for which recommendations are provided
        user_question (str): The user's question or query about agricultural actions.
        details (str): The detailed recommendations or actions suggested for the parcel
    """

    model: ImplementedModels
    project_id: str
    parcel_id: str
    user_question: str
    details: str
