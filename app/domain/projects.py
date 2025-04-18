from pydantic import BaseModel
from typing import List

from app.models.project import ProjectDetails
from app.services.projects_info import ProjectInfoService


class ProjectDomain(BaseModel):
    """
    A domain class that handles project-related operations and business logic.

    This class serves as an intermediary between the service layer and the application,
    providing a clean interface for project-related operations. It uses ProjectInfoService
    to interact with the underlying data layer.

    Attributes:
        projects_info (ProjectInfoService): An instance of ProjectInfoService used to
            interact with project data.
    """

    projects_info: ProjectInfoService = ProjectInfoService()

    def get_projects(self) -> List[ProjectDetails]:
        """
        Retrieves a list of all projects.

        Returns:
            List[ProjectDetails]: A list of ProjectDetails objects containing information
                about all available projects.
        """

        return self.projects_info.get_projects()

    def get_project(self, project_id: str) -> ProjectDetails | None:
        """
        Retrieves details of a specific project by its ID.

        Args:
            project_id (str): The unique identifier of the project to retrieve.

        Returns:
            ProjectDetails: A ProjectDetails object containing information about the
                requested project.
        """

        return self.projects_info.get_project(project_id)

    def get_project_by_parcel_id(self, parcel_id: str) -> ProjectDetails | None:
        """
        Retrieves details of a project by its parcel ID.

        Args:
            parcel_id (str): The unique identifier of the parcel to retrieve.

        Returns:
            ProjectDetails | None: A ProjectDetails object containing information about the
                requested project.
        """

        return self.projects_info.get_project_by_parcel_id(parcel_id)
