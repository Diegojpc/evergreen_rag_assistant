from pydantic import BaseModel
import datetime as dt
import random as rand

from app.models.process import ProcessInformation


class ProcessInformationService(BaseModel):
    """
    A service class that provides process information for agricultural parcels.

    This service simulates sensor data for agricultural monitoring by generating
    random values within realistic ranges for various environmental parameters.
    The service includes a 30% chance of returning None to simulate sensor failures
    or missing data scenarios.

    Attributes:
        Inherits from Pydantic BaseModel for data validation and serialization.
    """

    def get_process_information(self, parcel_id: str) -> ProcessInformation | None:
        """
        Retrieves simulated process information for a specific agricultural parcel.

        This method generates random sensor readings for various environmental parameters
        including soil moisture, temperatures, and conductivity measurements. There is a
        30% chance that the method will return None to simulate sensor failures or missing
        data scenarios.

        Args:
            parcel_id (str): The unique identifier of the agricultural parcel.

        Returns:
            ProcessInformation | None: A ProcessInformation object containing simulated
            sensor data if successful, or None if the simulation indicates a failure
            or missing data scenario.

        Note:
            The generated values are within realistic ranges:
            - Soil moisture: 35-65%
            - Soil temperature: 18-26°C
            - Air temperature: 20-30°C
            - Conductivity: 1.0-2.5 mS/cm
        """
        if rand.randint(0, 9) >= 7:
            return None

        timestamp: dt.datetime = dt.datetime.now()
        soil_moisture_percent: float = rand.uniform(35.0, 65.0)
        soil_temperature_c: float = rand.uniform(18.0, 26.0)
        air_temperature_c: float = rand.uniform(20.0, 30.0)
        conductivity_ms_cm: float = rand.uniform(1.0, 2.5)
        conductivity_ec_ms_cm: float = rand.uniform(1.0, 2.5)

        return ProcessInformation(
            parcel_id=parcel_id,
            timestamp=timestamp,
            soil_moisture_percent=soil_moisture_percent,
            soil_temperature_c=soil_temperature_c,
            air_temperature_c=air_temperature_c,
            conductivity_ms_cm=conductivity_ms_cm,
            conductivity_ec_ms_cm=conductivity_ec_ms_cm,
        )
