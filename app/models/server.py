from pydantic import BaseModel
from datetime import datetime

SERVER_STATUS_OK: str = "OK"


class ServerHealth(BaseModel):
    """
    A model representing the health status of the server.

    This class provides information about the current state of the server,
    including its status, a descriptive message, and the timestamp of the last check.

    Attributes:
        status (str): The current status of the server. Use SERVER_STATUS_OK for healthy state.
        message (str): A descriptive message about the server's state.
        timestamp (datetime): The time when the health check was performed.

    Example:
        >>> health = ServerHealth(status=SERVER_STATUS_OK, message="All systems operational")
        >>> health.status
        'OK'
    """

    status: str
    message: str
    timestamp: datetime

    def __init__(self, status: str, message: str):
        """
        Initialize a new ServerHealth instance.

        Args:
            status (str): The current status of the server.
            message (str): A descriptive message about the server's state.

        Note:
            The timestamp is automatically set to the current time when the instance is created.
        """
        timestamp = datetime.now()
        super().__init__(status=status, message=message, timestamp=timestamp)
