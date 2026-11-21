from threading import RLock
from uuid import UUID

from app.models.deployment import DeploymentCandidate


class DeploymentRepository:
    """Thread-safe in-memory persistence for deployment candidates."""

    def __init__(self) -> None:
        self._deployments: dict[UUID, DeploymentCandidate] = {}

        # FastAPI can execute synchronous endpoint work on worker threads.
        # Protect shared in-memory state from concurrent access.
        self._lock = RLock()

    def save(self, deployment: DeploymentCandidate) -> DeploymentCandidate:
        """Persist and return a deployment candidate."""

        with self._lock:
            self._deployments[deployment.id] = deployment

        return deployment

    def get_by_id(self, deployment_id: UUID) -> DeploymentCandidate | None:
        """Return the deployment when present; otherwise return None."""

        with self._lock:
            return self._deployments.get(deployment_id)
