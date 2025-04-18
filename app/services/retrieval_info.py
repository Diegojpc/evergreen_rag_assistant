from pydantic import BaseModel
from typing import List

from app.models.best_practices import BestIrrigationPractices, BestAgriculturalPractices
from app.models.project import HistoricalInformation


class RetrievalInfoService(BaseModel):
    """Service class for retrieving agricultural and irrigation best practices information.

    This service provides methods to access various types of agricultural information
    including irrigation best practices, crop-specific agricultural practices, and
    historical information about specific parcels.
    """

    def get_best_irrigation_practices(self) -> BestIrrigationPractices:
        """Retrieves a list of best practices for irrigation.

        Returns:
            BestIrrigationPractices: An object containing a list of recommended
            irrigation practices for optimal crop growth and water efficiency.
        """

        return BestIrrigationPractices(
            practices=[
                "Drip irrigation is the most efficient for most horticultural crops",
                "Measuring soil moisture (with sensors or manual methods) is key to adjusting dosages",
                "Consider evapotranspiration (ETo) and crop coefficient (Kc) to calculate water needs",
                "Avoid watering leaves during daylight hours to prevent sunburn and fungal diseases",
                "Controlled water stress in the final stages of some fruits (tomatoes, grapes) can improve quality, but is risky",
            ],
        )

    def get_best_agricultural_practices(
        self,
        crop_type: str,
        current_phase: str,
    ) -> BestAgriculturalPractices | None:
        """Retrieves best agricultural practices for a specific crop and growth phase.

        Args:
            crop_type (str): The type of crop (e.g., 'rice', 'cotton', 'barley').
            current_phase (str): The current growth phase of the crop (e.g., 'vegetative', 'flowering', 'maturity').

        Returns:
            BestAgriculturalPractices | None: An object containing recommended practices for the specified
            crop and phase, or None if no matching practices are found.
        """

        practices: List[BestAgriculturalPractices] = [
            BestAgriculturalPractices(
                crop_type="rice",
                current_phase="vegetative",
                practices=[
                    "Maintain optimal water depth of 5-10 cm during vegetative phase",
                    "Apply nitrogen fertilizer in split doses to support leaf growth",
                    "Monitor and control weeds to prevent nutrient competition",
                ],
            ),
            BestAgriculturalPractices(
                crop_type="cotton",
                current_phase="flowering",
                practices=[
                    "Ensure adequate water supply to prevent stress",
                    "Apply balanced fertilizers to support growth and yield",
                    "Control pests and diseases to maintain healthy plants",
                ],
            ),
            BestAgriculturalPractices(
                crop_type="barley",
                current_phase="maturity",
                practices=[
                    "Maintain optimal soil moisture levels",
                    "Apply balanced fertilizers to support growth and yield",
                    "Monitor and control pests and diseases",
                ],
            ),
        ]

        for practice in practices:
            if (
                practice.crop_type == crop_type
                and practice.current_phase == current_phase
            ):
                return practice

        return None

    def get_historical_information_by_parcel_id(
        self, parcel_id: str
    ) -> List[HistoricalInformation]:
        """Retrieves historical information for a specific agricultural parcel.

        Args:
            parcel_id (str): The unique identifier of the parcel.

        Returns:
            List[HistoricalInformation]: A list of historical information records for the specified parcel,
            including details about crops grown, planting dates, issues encountered, and notes.
        """

        historical_information: List[HistoricalInformation] = [
            HistoricalInformation(
                year=2023,
                parcel_id="P1233",
                crop_type="cotton",
                planting_date="2023-04-12",
                issues="Drought and pests",
                notes="The crop was affected by pests and drought, resulting in a lower yield.",
            ),
            HistoricalInformation(
                year=2023,
                parcel_id="P1234",
                crop_type="rice",
                planting_date="2023-02-23",
                issues="None",
                notes="Excellent growing season with optimal conditions throughout. Achieved higher than expected yield.",
            ),
            HistoricalInformation(
                year=2023,
                parcel_id="P1235",
                crop_type="barley",
                planting_date="2023-05-19",
                issues="Drought and pests",
                notes="The crop was affected by pests and drought, resulting in a lower yield.",
            ),
        ]

        return [info for info in historical_information if info.parcel_id == parcel_id]
