from pydantic import BaseModel
import datetime as dt
import random as rand

from app.models.lunar import LunarAnalysis, LunarPhase


class LunarInfoService(BaseModel):
    """
    A service class that provides lunar information and analysis for agricultural parcels.

    This service simulates lunar data retrieval and analysis, including moon phase and illumination.
    It's designed to be used in agricultural applications where lunar cycles may be relevant
    for farming decisions.

    Attributes:
        Inherits from Pydantic BaseModel for data validation and serialization.
    """

    def get_lunar_info(self) -> LunarAnalysis | None:
        """
        Retrieves lunar analysis information for a specific agricultural parcel.

        This method simulates retrieving lunar data with a random chance of failure.
        When successful, it returns a LunarAnalysis object containing the current moon phase
        and illumination percentage.

        Args:
            None

        Returns:
            LunarAnalysis | None: A LunarAnalysis object containing:
                - timestamp: Current datetime
                - phase: Current moon phase (currently hardcoded to NEW)
                - illumination_percent: Random illumination percentage between 0 and 100
            Returns None with a 30% probability to simulate service unreliability.

        Note:
            This is a simulation implementation that returns random data. In a production
            environment, this would connect to a real lunar data service or database.
        """
        if rand.randint(0, 9) >= 7:
            return None

        timestamp: dt.datetime = dt.datetime.now()
        phase: LunarPhase = LunarPhase.NEW
        illumination_percent: float = rand.uniform(0.0, 100.0)

        return LunarAnalysis(
            timestamp=timestamp,
            phase=phase,
            illumination_percent=illumination_percent,
        )
