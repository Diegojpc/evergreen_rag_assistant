from pydantic import BaseModel


class HistoricalInformation(BaseModel):
    """A data model representing historical agricultural information for a specific parcel.

    This class stores historical farming data for a particular parcel, including crop
    information, planting dates, and any issues or notes from previous growing seasons.
    It inherits from Pydantic's BaseModel to provide data validation and serialization.

    Attributes:
        year (int): The year when the historical data was recorded
        parcel_id (str): Unique identifier for the specific plot/field
        crop_type (str): Type of crop that was cultivated (e.g., corn, wheat, soybeans)
        planting_date (str): Date when the crop was planted in YYYY-MM-DD format
        issues (str): Any problems or challenges encountered during the growing season
        notes (str): Additional observations or important information about the season
    """

    year: int
    parcel_id: str
    crop_type: str
    planting_date: str
    issues: str
    notes: str

    def to_prompt_string(self) -> str:
        """Convert the historical information into a formatted string suitable for use in prompts.

        This method formats all the historical information into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all historical information, with each field on a new line.
                 The string includes year, parcel ID, crop type, planting date, issues, and notes.
        """

        return f"""
                - Year: {self.year}
                - Parcel ID: {self.parcel_id}
                - Crop Type: {self.crop_type}
                - Planting Date: {self.planting_date}
                - Issues: {self.issues}
                - Notes: {self.notes}
        """


class ProjectDetails(BaseModel):
    """
    A data model representing the details of an agricultural project.

    This class encapsulates essential information about a farming project, including
    identification details, crop information, and current status.

    Attributes:
        project_id (str): Unique identifier for the project
        parcel_id (str): Identifier for the specific plot/field where the crop is planted
        location (str): Location of the project
        crop_type (str): Type of crop being cultivated (e.g., corn, wheat, soybeans)
        variety (str): Specific variety or cultivar of the crop
        planting_date (str): Date when the crop was planted (format: YYYY-MM-DD)
        current_phase (str): Current growth or development phase of the crop
    """

    project_id: str
    parcel_id: str
    location: str
    crop_type: str
    variety: str
    planting_date: str
    current_phase: str

    def to_prompt_string(self) -> str:
        """Convert the project details into a formatted string suitable for use in prompts.

        This method formats all the project details into a human-readable string that can be used
        as context in prompts or for display purposes. Each field is presented on a new line with
        a clear label.

        Returns:
            str: A formatted string containing all project details, with each field on a new line.
                 The string includes project ID, parcel ID, location, crop type, variety,
                 planting date, and current phase.
        """

        return f"""
            - Project ID: {self.project_id}
            - Parcel ID: {self.parcel_id}
            - Location: {self.location}
            - Crop Type: {self.crop_type}
            - Variety: {self.variety}
            - Planting Date: {self.planting_date}
            - Current Phase: {self.current_phase}
        """
