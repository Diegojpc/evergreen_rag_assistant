from fastapi import APIRouter

from app.models.server import ServerHealth, SERVER_STATUS_OK

health_router: APIRouter = APIRouter(
    prefix="/server",
    tags=["Server"],
)


@health_router.get(
    path="/status",
    description="Health check endpoint for the server",
    response_model=ServerHealth,
)
def verify_server_status() -> ServerHealth:
    """
    Health check endpoint for the server.

    This endpoint is used to verify that the server is running and operational.
    It returns a simple health status response indicating the server's current state.

    Returns:
        ServerHealth: A response object containing:
            - status: The server status (typically "OK" when running normally)
            - message: A descriptive message about the server's state
            - timestamp: The timestamp of the health check verification
    """

    return ServerHealth(
        status=SERVER_STATUS_OK, message="Server is running and ready to be used"
    )
