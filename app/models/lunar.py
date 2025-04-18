from pydantic import BaseModel
import datetime as dt
from enum import Enum


class LunarPhase(Enum):
    """
    Enumeration representing the different phases of the moon.

    Attributes:
        NEW: Represents the new moon phase when the moon is not visible
        CRESCENT: Represents the crescent moon phase
        FULL: Represents the full moon phase
        WANING: Represents the waning moon phase
    """

    NEW = "New"
    CRESCENT = "Crescent"
    FULL = "Full"
    WANING = "Waning"


class LunarAnalysis(BaseModel):
    """
    A data model representing lunar analysis data at a specific point in time.

    Attributes:
        timestamp: The date and time when the lunar analysis was performed
        phase: The current phase of the moon according to the LunarPhase enum
        illumination_percent: The percentage of the moon's surface that is illuminated
            (ranges from 0 to 100)
    """

    timestamp: dt.datetime
    phase: LunarPhase
    illumination_percent: float

    def to_prompt_string(self) -> str:
        """Convert the lunar analysis into a formatted string suitable for use in prompts.

        This method formats all the lunar analysis data into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all lunar analysis data, with each field on a new line.
                 The string includes timestamp, phase, and illumination percentage.
        """

        return f"""
        - Timestamp: {self.timestamp}
        - Phase: {self.phase}
        - Illumination Percent: {self.illumination_percent}%
        """
