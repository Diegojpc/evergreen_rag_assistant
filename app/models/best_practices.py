from pydantic import BaseModel
from typing import List


class BestIrrigationPractices(BaseModel):
    """
    A Pydantic model representing a collection of best irrigation practices.

    This model is used to structure and validate data related to recommended irrigation
    practices. It stores a list of practice descriptions that can be used for
    agricultural or landscaping purposes.

    Attributes:
        practices (List[str]): A list of strings, where each string represents
            a specific irrigation practice or recommendation.
    """

    practices: List[str]

    def to_prompt_string(self) -> str:
        """Convert the best irrigation practices into a formatted string suitable for use in prompts.

        This method formats all the best irrigation practices into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all best irrigation practices, with each field on a new line.
                 The string includes practices.
        """
        if len(self.practices) == 0:
            practices_str: str = "No best irrigation practices available"
        else:
            practices_str = """
            """.join([practice for practice in self.practices])

        return practices_str


class BestAgriculturalPractices(BaseModel):
    """
    A Pydantic model representing a collection of best agricultural practices for a specific crop type.

    This model is used to structure and validate data related to recommended agricultural
    practices for different types of crops. It associates a specific crop type with a
    list of relevant best practices.

    Attributes:
        crop_type (str): The type of crop these practices are recommended for.
        current_phase (str): The current phase of the crop.
        practices (List[str]): A list of strings, where each string represents
            a specific agricultural practice or recommendation for the given crop type.
    """

    crop_type: str
    current_phase: str
    practices: List[str]

    def to_prompt_string(self) -> str:
        """Convert the best agricultural practices into a formatted string suitable for use in prompts.

        This method formats all the best agricultural practices into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all best agricultural practices, with each field on a new line.
                 The string includes crop type, current phase, and practices.
        """
        if len(self.practices) == 0:
            practices_str: str = "No best agricultural practices available"
        else:
            practices_str = """
            """.join([practice for practice in self.practices])

        return f"""
        - Crop Type: {self.crop_type}
        - Current Phase: {self.current_phase}
        - Practices:
            {practices_str}
        """
