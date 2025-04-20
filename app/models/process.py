import datetime as dt
from pydantic import BaseModel


class ProcessInformation(BaseModel):
    """
    A data model representing environmental process information for agricultural monitoring.

    This model captures key environmental parameters that are crucial for monitoring
    and managing agricultural processes, particularly for soil and environmental conditions.

    Attributes:
        parcel_id (str): The ID of the parcel
        timestamp (datetime): The timestamp when the measurements were taken
        soil_moisture_percent (float): Soil moisture content expressed as a percentage
        soil_temperature_c (float): Soil temperature in degrees Celsius
        air_temperature_c (float): Ambient air temperature in degrees Celsius
        conductivity_ms_cm (float): Soil conductivity in millisiemens per centimeter
        conductivity_ec_ms_cm (float): Electrical conductivity of the soil in millisiemens per centimeter
    """

    parcel_id: str
    timestamp: dt.datetime
    soil_moisture_percent: float
    soil_temperature_c: float
    air_temperature_c: float
    conductivity_ms_cm: float
    conductivity_ec_ms_cm: float

    def to_prompt_string(self) -> str:
        """Convert the process information into a formatted string suitable for use in prompts.

        This method formats all the process information into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all process information, with each field on a new line.
                 The string includes parcel ID, timestamp, soil moisture, soil temperature, air temperature,
                 conductivity, and electrical conductivity.
        """

        return f"""
            - Parcel ID: {self.parcel_id}
            - Timestamp: {self.timestamp}
            - Soil Moisture: {self.soil_moisture_percent}%
            - Soil Temperature: {self.soil_temperature_c}°C
            - Air Temperature: {self.air_temperature_c}°C
            - Conductivity: {self.conductivity_ms_cm} mS/cm
            - Electrical Conductivity: {self.conductivity_ec_ms_cm} mS/cm
        """
