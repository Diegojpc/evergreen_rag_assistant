from pydantic import BaseModel
import datetime as dt
import random as rand

from app.models.satellite import (
    SatelliteImageAnalysis,
    SatelliteImageAnalysisStatus,
    Anomality,
)


class SatelliteInfoService(BaseModel):
    """
    A service class that provides satellite image analysis information for agricultural parcels.

    This service simulates satellite data retrieval and analysis for agricultural monitoring.
    It provides information about vegetation coverage and potential issues detected in satellite imagery.

    Attributes:
        Inherits from Pydantic BaseModel for data validation and serialization.
    """

    def get_satellite_info(self, parcel_id: str) -> SatelliteImageAnalysis | None:
        """
        Retrieves satellite image analysis information for a specific agricultural parcel.

        This method simulates satellite data retrieval with a 30% chance of returning no data
        (simulating cloud cover or other data unavailability). When data is available, it returns
        analysis including vegetation coverage percentage and potential issues.

        Args:
            parcel_id (str): The unique identifier of the agricultural parcel to analyze.

        Returns:
            SatelliteImageAnalysis | None:
                - If data is available: Returns a SatelliteImageAnalysis object containing:
                    - timestamp: Current time of analysis
                    - status: Current status of the parcel (NORMAL by default)
                    - detected_issue: Any issues detected (None by default)
                    - coverage_percent: Random vegetation coverage between 70% and 95%
                - If no data is available: Returns None (30% chance)
        """
        if rand.randint(0, 9) >= 7:
            return None

        status: SatelliteImageAnalysisStatus = rand.choice(
            list(SatelliteImageAnalysisStatus)
        )

        detected_issue: Anomality | None = None
        if status != SatelliteImageAnalysisStatus.NORMAL:
            detected_issue = rand.choice(list(Anomality))

        timestamp: dt.datetime = dt.datetime.now()
        coverage_percent: float = rand.uniform(10.0, 95.0)

        return SatelliteImageAnalysis(
            parcel_id=parcel_id,
            timestamp=timestamp,
            status=status,
            detected_issue=detected_issue,
            coverage_percent=coverage_percent,
        )
