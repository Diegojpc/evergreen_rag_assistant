from fastapi import APIRouter, Path
from typing import List

from app.models.project import ProjectDetails
from app.domain.projects import ProjectDomain


projects_router: APIRouter = APIRouter(
    prefix="/projects",
    tags=["Agricultural Projects"],
)

projects_domain: ProjectDomain = ProjectDomain()


@projects_router.get(
    path="/",
    description="Get all agricultural projects",
    response_model=List[ProjectDetails],
)
def get_projects() -> List[ProjectDetails]:
    """
    Retrieve a list of all agricultural projects with optional filtering.

    This endpoint returns a comprehensive list of all agricultural projects stored in the system.
    Each project in the list contains detailed information about the agricultural initiative.
    Results can be filtered and paginated using query parameters.

    Args:
        status (Optional[str]): Filter projects by their status (e.g., 'active', 'completed', 'planned').
        region (Optional[str]): Filter projects by geographical region.
        limit (Optional[int]): Maximum number of projects to return (default: 100, max: 1000).
        offset (Optional[int]): Number of projects to skip for pagination (default: 0).

    Returns:
        List[ProjectDetails]: A list of ProjectDetails objects, each representing an agricultural project
            with its complete set of attributes and metadata.
    """

    return projects_domain.get_projects()


@projects_router.get(
    path="/{project_id}",
    description="Get a specific agricultural project by ID",
    response_model=ProjectDetails | None,
)
def get_project_by_id(
    project_id: str = Path(
        ...,
        description="The unique identifier of the agricultural project to retrieve.",
    ),
) -> ProjectDetails | None:
    """
    Retrieve detailed information about a specific agricultural project.

    This endpoint returns comprehensive details about a particular agricultural project
    identified by its unique project ID. If the project is not found, returns None.

    Args:
        project_id (str): The unique identifier of the agricultural project to retrieve.

    Returns:
        ProjectDetails | None: A ProjectDetails object containing all information about the requested
            agricultural project, or None if the project is not found.
    """

    return projects_domain.get_project(project_id)


@projects_router.get(
    path="/parcel/{parcel_id}",
    description="Get a specific agricultural project by parcel ID",
    response_model=ProjectDetails | None,
)
def get_project_by_parcel_id(
    parcel_id: str = Path(
        ...,
        description="The unique identifier of the parcel to retrieve.",
    ),
) -> ProjectDetails | None:
    """
    Retrieve detailed information about a specific agricultural project by its parcel ID.

    This endpoint returns comprehensive details about a particular agricultural project
    identified by its unique parcel ID. If the project is not found, returns None.

    Args:
        parcel_id (str): The unique identifier of the parcel to retrieve.

    Returns:
        ProjectDetails | None: A ProjectDetails object containing all information about the requested
            agricultural project, or None if the project is not found.
    """

    return projects_domain.get_project_by_parcel_id(parcel_id)
