from fastapi import HTTPException
from typing import List
from pydantic import BaseModel

from app.models.project import ProjectDetails, HistoricalInformation
from app.models.best_practices import BestIrrigationPractices, BestAgriculturalPractices
from app.models.recommendations import RecommendationRequest, RecommendationResponse
from app.models.process import ProcessInformation
from app.models.lunar import LunarAnalysis
from app.models.satellite import SatelliteImageAnalysis
from app.models.weather import WeatherForecast
from app.models.llms import ImplementedModels
from app.services.projects_info import ProjectInfoService
from app.services.process_info import ProcessInformationService
from app.services.lunar_info import LunarInfoService
from app.services.satellite_info import SatelliteInfoService
from app.services.weather_info import WeatherInformationService
from app.services.retrieval_info import RetrievalInfoService
from app.services.llms import LLMsService


class RecommendationDomain(BaseModel):
    projects_service: ProjectInfoService = ProjectInfoService()
    process_service: ProcessInformationService = ProcessInformationService()
    lunar_service: LunarInfoService = LunarInfoService()
    satellite_service: SatelliteInfoService = SatelliteInfoService()
    weather_service: WeatherInformationService = WeatherInformationService()
    retrieval_service: RetrievalInfoService = RetrievalInfoService()
    llms_service: LLMsService = LLMsService()

    def build_prompt(
        self,
        user_question: str,
        project_details: ProjectDetails,
        process_info: ProcessInformation | None,
        lunar_analysis: LunarAnalysis | None,
        satellite_analysis: SatelliteImageAnalysis | None,
        weather_forecast: WeatherForecast | None,
        best_irrigation_practices: BestIrrigationPractices | None,
        best_agricultural_practices: BestAgriculturalPractices | None,
        historical_information: List[HistoricalInformation] | None,
    ) -> str:
        project_details_str: str = project_details.to_prompt_string()

        process_info_str: str = (
            process_info.to_prompt_string() if process_info else "Not available"
        )

        satellite_analysis_str: str = (
            satellite_analysis.to_prompt_string()
            if satellite_analysis
            else "Not available"
        )

        weather_forecast_str: str = (
            weather_forecast.to_prompt_string() if weather_forecast else "Not available"
        )

        best_irrigation_practices_str: str = (
            best_irrigation_practices.to_prompt_string()
            if best_irrigation_practices
            else "Not available"
        )

        best_agricultural_practices_str: str = (
            best_agricultural_practices.to_prompt_string()
            if best_agricultural_practices
            else "Not available"
        )

        if len(historical_information) == 0:
            historical_information_str: str = "No historical information available"
        else:
            historical_information_str = """
            """.join(
                [
                    historical_information.to_prompt_string()
                    for historical_information in historical_information
                ]
            )

        user_prompt: str = f"""User/System Request: {user_question}"""

        system_prompt: str = f"""
        You are a virtual expert Agronomist Assistant for the Evergreen system. Your goal is to provide contextualized, proactive, and evidence-based recommendations for crop management.

        Use the following contextual information to generate your response:
        1. **Crop/Project Details:**
        {project_details_str}
        2. **Process Information (if available):**
        {process_info_str}
        3. **Recent Image Analysis (if available):**
        {satellite_analysis_str}
        4. **Weather Forecast:**
        {weather_forecast_str}
        5. **Moon Phase (optional additional context):**
        {lunar_analysis}
        6. **Retrieved Agronomic Knowledge (manuals, history, best practices):**
        {best_irrigation_practices_str}
        {best_agricultural_practices_str}
        {historical_information_str}
        
        Key Instructions for Your Response:
        - Prioritize the most urgent or impactful actions.
        - Be concise but clear in your recommendations and justifications.
        - Base your justifications explicitly on the data provided (sensors, weather, images, history, manuals). Mention the source if relevant (e.g., 'according to manual', 'due to forecast').
        - If you detect risks (pests, diseases, adverse weather), include them in the 'warnings' section.
        - If there is no sensor or image data, indicate this and base your recommendations on the rest of the information.
        - If the question is very general (e.g., 'what to do?'), focus on the key next actions for the current crop phase and conditions.
        - The default time horizon is the next week, unless the question specifies otherwise.

        {user_prompt}
        """

        print(system_prompt)

        return system_prompt

    def get_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationResponse:
        project_details: ProjectDetails | None = (
            self.projects_service.get_project_by_parcel_id(parcel_id=request.parcel_id)
        )

        if project_details is None:
            raise HTTPException(
                status_code=404,
                detail=f"Project not found for parcel ID {request.parcel_id}",
            )

        process_info: ProcessInformation | None = (
            self.process_service.get_process_information(parcel_id=request.parcel_id)
        )

        lunar_analysis: LunarAnalysis | None = self.lunar_service.get_lunar_info()

        satellite_analysis: SatelliteImageAnalysis | None = (
            self.satellite_service.get_satellite_info(parcel_id=request.parcel_id)
        )

        weather_forecast: WeatherForecast | None = (
            self.weather_service.get_weather_forecast(location=project_details.location)
        )

        best_irrigation_practices: BestIrrigationPractices | None = (
            self.retrieval_service.get_best_irrigation_practices()
        )

        best_agricultural_practices: BestAgriculturalPractices | None = (
            self.retrieval_service.get_best_agricultural_practices(
                crop_type=project_details.crop_type,
                current_phase=project_details.current_phase,
            )
        )

        historical_information: List[HistoricalInformation] | None = (
            self.retrieval_service.get_historical_information_by_parcel_id(
                parcel_id=request.parcel_id,
            )
        )

        prompt: str = self.build_prompt(
            user_question=request.user_question,
            project_details=project_details,
            process_info=process_info,
            lunar_analysis=lunar_analysis,
            satellite_analysis=satellite_analysis,
            weather_forecast=weather_forecast,
            best_irrigation_practices=best_irrigation_practices,
            best_agricultural_practices=best_agricultural_practices,
            historical_information=historical_information,
        )

        if request.model in [
            ImplementedModels.FLAN_T5_LARGE,
            ImplementedModels.FALCON_RW_1B,
            ImplementedModels.GPT_NEO_1_3B,
        ]:
            try:
                response: str = self.llms_service.query_huggingface_model(
                    model=request.model,
                    prompt=prompt,
                )

                return RecommendationResponse(
                    model=ImplementedModels.FLAN_T5_LARGE,
                    project_id=project_details.project_id,
                    parcel_id=request.parcel_id,
                    user_question=request.user_question,
                    details=response,
                )

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error querying LLM: {e}",
                )

        raise HTTPException(
            status_code=400,
            detail=f"Requested LLM '{request.model}' not implemented",
        )
