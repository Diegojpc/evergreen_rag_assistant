from fastapi import HTTPException
from typing import List
from pydantic import BaseModel, Field
import logging

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationDomain(BaseModel):
    projects_service: ProjectInfoService = ProjectInfoService()
    process_service: ProcessInformationService = ProcessInformationService()
    lunar_service: LunarInfoService = LunarInfoService()
    satellite_service: SatelliteInfoService = SatelliteInfoService()
    weather_service: WeatherInformationService = WeatherInformationService()
    retrieval_service: RetrievalInfoService = RetrievalInfoService()
    llms_service: LLMsService = LLMsService()

    def build_system_prompt(
        self,
        project_details: ProjectDetails,
        process_info: ProcessInformation | None,
        lunar_analysis: LunarAnalysis | None,
        satellite_analysis: SatelliteImageAnalysis | None,
        weather_forecast: WeatherForecast | None,
        best_irrigation_practices: BestIrrigationPractices | None,
        best_agricultural_practices: BestAgriculturalPractices | None,
        historical_information: List[HistoricalInformation] | None,
    ) -> str:
        """Builds the system part of the prompt containing context and instructions."""
        project_details_str: str = project_details.to_prompt_string()

        process_info_str: str = (
            process_info.to_prompt_string() if process_info else "Not available"
        )
        
        lunar_analysis_str: str = (
             lunar_analysis.to_prompt_string() if lunar_analysis else "Not available"
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
            historical_information_str = "\n".join(
                [info.to_prompt_string() for info in historical_information]
            )

        system_prompt: str = f"""
        You are a virtual expert Agronomist Assistant for the Evergreen system. Your goal is to provide contextualized, proactive, and evidence-based recommendations for crop management.

        Use the following contextual information to generate your response:
        1.  **Crop/Project Details:**
        {project_details_str}
        2.  **Process Information (Sensors, if available):**
        {process_info_str}
        3.  **Recent Satellite Image Analysis (if available):**
        {satellite_analysis_str}
        4.  **Weather Forecast:**
        {weather_forecast_str}
        5.  **Moon Phase (optional additional context):**
        {lunar_analysis_str}
        6.  **Retrieved Agronomic Knowledge (Best Practices & History):**
            - Best Irrigation Practices:
        {best_irrigation_practices_str}
            - Best Agricultural Practices for Crop/Phase:
        {best_agricultural_practices_str}
            - Historical Information for this Parcel:
        {historical_information_str}

        Key Instructions for Your Response:
        - Prioritize the most urgent or impactful actions for the next 5-7 days unless otherwise specified by the user.
        - Be concise but clear in your recommendations and justifications.
        - Base your justifications explicitly on the data provided (sensors, weather, images, history, best practices). Mention the source if relevant (e.g., 'according to best practices', 'due to weather forecast indicating high humidity', 'based on low soil moisture sensor readings').
        - If you detect risks (pests, diseases, adverse weather based on forecast or satellite data), clearly state them as warnings.
        - If sensor or image data is unavailable, state this limitation and base recommendations on available data (project details, weather, knowledge).
        - Structure the output clearly, perhaps using bullet points for recommendations and warnings.
        - Respond directly to the user's request/question provided below.
                """
        return system_prompt.strip()

    def get_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationResponse:
        """Fetches context, builds prompt, queries the selected LLM, and returns the response."""
        logger.info(f"Starting recommendation process for parcel: {request.parcel_id} using model: {request.model.value}")
        
        # 1. Obtener Detalles del Proyecto
        project_details: ProjectDetails | None = (
            self.projects_service.get_project_by_parcel_id(parcel_id=request.parcel_id)
        )

        if project_details is None:
            logger.warning(f"Project not found for parcel ID {request.parcel_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Project not found for parcel ID {request.parcel_id}",
            )
        logger.info(f"Project details found: {project_details.project_id}")

        # 2. Obtener Datos de Contexto Adicionales (Sensores, Satélite, Clima, etc.)
        try:
            logger.info("Fetching context data...")
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
            logger.info("Context data fetched successfully.")
        except Exception as e:
             logger.error(f"Error fetching context data for parcel {request.parcel_id}: {e}", exc_info=True)
             raise HTTPException(status_code=503, detail=f"Failed to fetch context data: {e}")
         
        # 3. Construir el Prompt (Separando System y User)
        logger.info("Building prompt...")
        system_prompt: str = self.build_system_prompt(
            project_details=project_details,
            process_info=process_info,
            lunar_analysis=lunar_analysis,
            satellite_analysis=satellite_analysis,
            weather_forecast=weather_forecast,
            best_irrigation_practices=best_irrigation_practices,
            best_agricultural_practices=best_agricultural_practices,
            historical_information=historical_information,
        )
        
        user_prompt: str = request.user_question
        logger.info("Prompt built.")

        # 4. Seleccionar y Consultar el LLM
        response_text: str = ""
        try:
            if request.model in [
                ImplementedModels.FLAN_T5_LARGE,
                ImplementedModels.FALCON_RW_1B,
                ImplementedModels.GPT_NEO_1_3B
            ]:
                 logger.info(f"Querying Hugging Face model: {request.model.value}")
                 # Para HF, combinamos prompts por ahora, o adaptamos el servicio HF si queremos separación
                 full_hf_prompt = system_prompt + "\n\nUser/System Request: " + user_prompt
                 response_text = self.llms_service.query_huggingface_model(
                    model=request.model,
                    prompt=full_hf_prompt, # Pasar prompt combinado
                 )

            elif request.model == ImplementedModels.GPT_OPENAI_4O:
                 logger.info(f"Querying OpenAI model: {request.model.value}")
                 response_text = self.llms_service.query_openai_model(
                    model=request.model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                 )
            else:
                logger.error(f"Requested LLM '{request.model}' not implemented.")
                raise HTTPException(
                    status_code=400,
                    detail=f"Requested LLM '{request.model.value}' not implemented or supported.",
                )

            logger.info(f"LLM ({request.model.value}) generated response.")
            

        except RuntimeError as e:
            logger.error(f"LLM service failed: {e}", exc_info=True)
            raise HTTPException(status_code=503, detail=f"LLM service error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during LLM query: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Internal server error during recommendation generation: {e}")


        # 5. Formatear y Devolver la Respuesta
        return RecommendationResponse(
            model=request.model,
            project_id=project_details.project_id,
            parcel_id=request.parcel_id,
            user_question=request.user_question,
            details=response_text,
        )
