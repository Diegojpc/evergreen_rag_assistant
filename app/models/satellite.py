from pydantic import BaseModel
import datetime as dt
from enum import Enum


class SatelliteImageAnalysisStatus(Enum):
    """
    Enumeration representing the possible statuses of a satellite image analysis.

    This enum defines the possible states that a satellite image analysis can be in,
    indicating whether the analyzed agricultural parcel shows normal conditions or
    if any anomalies have been detected.

    Values:
        NORMAL: Indicates that the analysis shows expected conditions with no detected issues
        ANOMALY_DETECTED: Indicates that the analysis has identified potential problems or
                         unusual patterns that require attention
    """

    NORMAL = "Normal"
    ANOMALY_DETECTED = "Anomaly Detected"


class Anomality(Enum):
    """
    Enumeration representing the possible anomalies that can be detected in a satellite image.
    """

    DROUGHT = "Drought Stress"
    PEST_INFESTATION = "Pest Infestation"
    NUTRIENT_DEFICIENCY = "Nutrient Deficiency"


class SatelliteImageAnalysis(BaseModel):
    """
    A model representing the analysis results of a satellite image for a specific agricultural parcel.

    This model captures key information about the analysis of satellite imagery, including
    the identification of potential issues, vegetation coverage, and the analysis status.

    Attributes:
        parcel_id (str): Unique identifier for the agricultural parcel being analyzed
        timestamp (datetime): The date and time when the analysis was performed
        status (SatelliteImageAnalysisStatus): Current status of the analysis
        detected_issue (str | None): Description of any issues detected in the analysis, if any
        coverage_percent (float): Percentage of vegetation coverage detected in the parcel
    """

    parcel_id: str
    timestamp: dt.datetime
    status: SatelliteImageAnalysisStatus
    detected_issue: Anomality | None
    coverage_percent: float

    def to_prompt_string(self) -> str:
        """Convert the satellite image analysis into a formatted string suitable for use in prompts.

        This method formats all the satellite image analysis data into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all satellite image analysis data, with each field on a new line.
                 The string includes parcel ID, timestamp, status, detected issue, and coverage percentage.
        """

        return f"""
        - Parcel ID: {self.parcel_id}
        - Timestamp: {self.timestamp}
        - Status: {self.status}
        - Detected Issue: {self.detected_issue}
        - Coverage Percent: {self.coverage_percent}%
        """
