from pydantic import BaseModel
from typing import List

from app.models.project import ProjectDetails


class ProjectInfoService(BaseModel):
    """
    A service class for managing project information and details.

    This class maintains a list of project details and provides methods to retrieve
    project information. It serves as a data store for project-related information
    including crop types, planting dates, and current growth phases.

    Attributes:
        Inherits from Pydantic BaseModel for data validation and serialization.
    """

    projects: List[ProjectDetails] = [
        ProjectDetails(
            project_id="PROJ_RICE_20240101_P1233",
            parcel_id="P1233",
            location="Ciudad Bolivar, Antioquia, Colombia",
            crop_type="rice",
            variety="jasmine",
            planting_date="2024-01-01",
            current_phase="vegetative",
        ),
        ProjectDetails(
            project_id="PROJ_COTTON_20240116_P1234",
            parcel_id="P1234",
            location="Hispania, Antioquia, Colombia",
            crop_type="cotton",
            variety="upland",
            planting_date="2024-01-16",
            current_phase="flowering",
        ),
        ProjectDetails(
            project_id="PROJ_BARLEY_20240202_P1235",
            parcel_id="P1235",
            location="Jardín, Antioquia, Colombia",
            crop_type="barley",
            variety="winter",
            planting_date="2024-02-02",
            current_phase="maturity",
        ),
    ]

    def get_projects(self) -> List[ProjectDetails]:
        """
        Retrieve all projects stored in the service.

        Returns:
            List[ProjectDetails]: A list containing all project details.
        """

        return self.projects

    def get_project(self, project_id: str) -> ProjectDetails | None:
        """
        Retrieve a specific project by its ID.

        Args:
            project_id (str): The unique identifier of the project to retrieve.

        Returns:
            ProjectDetails | None: The project details if found, None otherwise.
        """

        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None

    def get_project_by_parcel_id(self, parcel_id: str) -> ProjectDetails | None:
        """
        Retrieve a project by its parcel ID.

        Args:
            parcel_id (str): The unique identifier of the parcel to retrieve.

        Returns:
            ProjectDetails | None: The project details if found, None otherwise.
        """

        for project in self.projects:
            if project.parcel_id == parcel_id:
                return project
        return None
